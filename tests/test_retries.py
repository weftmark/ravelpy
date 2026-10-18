"""Tests for opt-in GET retries (``RavelryClient(max_retries=...)``)."""

import email.utils
import time

import httpx
import pytest
import pytest_asyncio

from ravelpy import RavelryAPIError, RavelryClient, RavelryConnectionError
from ravelpy import _retry


@pytest.fixture
def sleeps(monkeypatch):
    """Replace the retry sleep with a recorder so tests run instantly."""
    calls: list[float] = []

    async def _fake_sleep(delay: float) -> None:
        calls.append(delay)

    monkeypatch.setattr(_retry, "_sleep", _fake_sleep)
    return calls


@pytest_asyncio.fixture
async def retry_client():
    c = RavelryClient(username="u", api_key="k", max_retries=2)
    yield c
    await c.aclose()


@pytest.mark.asyncio
@pytest.mark.parametrize("exc", list(_retry.RETRY_EXCEPTIONS))
async def test_retries_transport_error_then_succeeds(retry_client, mock_api, sleeps, exc):
    route = mock_api.get("/color_families.json").mock(
        side_effect=[exc("flaky"), httpx.Response(200, json={"color_families": []})]
    )
    _, _, raw = await retry_client.extras.color_families()
    assert raw == {"color_families": []}
    assert route.call_count == 2
    assert len(sleeps) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("status", sorted(_retry.RETRY_STATUSES))
async def test_retries_status_then_succeeds(retry_client, mock_api, sleeps, status):
    route = mock_api.get("/color_families.json").mock(
        side_effect=[httpx.Response(status), httpx.Response(200, json={})]
    )
    await retry_client.extras.color_families()
    assert route.call_count == 2


@pytest.mark.asyncio
async def test_gives_up_after_max_retries_with_connection_error(retry_client, mock_api, sleeps):
    route = mock_api.get("/color_families.json").mock(side_effect=httpx.ReadTimeout("slow"))
    with pytest.raises(RavelryConnectionError) as excinfo:
        await retry_client.extras.color_families()
    assert excinfo.value.is_timeout
    assert route.call_count == 3  # 1 attempt + 2 retries
    assert len(sleeps) == 2


@pytest.mark.asyncio
async def test_gives_up_after_max_retries_with_api_error(retry_client, mock_api, sleeps):
    route = mock_api.get("/color_families.json").respond(503, text="down for maintenance")
    with pytest.raises(RavelryAPIError) as excinfo:
        await retry_client.extras.color_families()
    assert excinfo.value.status_code == 503
    assert excinfo.value.message == "down for maintenance"
    assert route.call_count == 3


@pytest.mark.asyncio
@pytest.mark.parametrize("status", [400, 401, 403, 404, 500])
async def test_does_not_retry_other_statuses(retry_client, mock_api, sleeps, status):
    route = mock_api.get("/color_families.json").respond(status)
    with pytest.raises(RavelryAPIError):
        await retry_client.extras.color_families()
    assert route.call_count == 1
    assert sleeps == []


@pytest.mark.asyncio
async def test_does_not_retry_success_or_304(retry_client, mock_api, sleeps):
    route = mock_api.get("/color_families.json").respond(304)
    await retry_client.extras.color_families(etag='"e"')
    assert route.call_count == 1
    assert sleeps == []


@pytest.mark.asyncio
async def test_post_never_retried(retry_client, mock_api, sleeps):
    route = mock_api.post("/people/u/stash/create.json").mock(side_effect=httpx.ReadTimeout("slow"))
    with pytest.raises(RavelryConnectionError):
        await retry_client.stash.create("u", {"yarn_id": 1})
    assert route.call_count == 1
    assert sleeps == []


@pytest.mark.asyncio
async def test_post_503_not_retried(retry_client, mock_api, sleeps):
    route = mock_api.post("/people/u/stash/create.json").respond(503)
    with pytest.raises(RavelryAPIError):
        await retry_client.stash.create("u", {"yarn_id": 1})
    assert route.call_count == 1


@pytest.mark.asyncio
async def test_default_client_does_not_retry(client, mock_api, sleeps):
    route = mock_api.get("/color_families.json").respond(503)
    with pytest.raises(RavelryAPIError):
        await client.extras.color_families()
    assert route.call_count == 1
    assert sleeps == []


@pytest.mark.asyncio
async def test_if_none_match_sent_on_every_attempt(retry_client, mock_api, sleeps):
    route = mock_api.get("/color_families.json").mock(
        side_effect=[httpx.ConnectError("x"), httpx.Response(503), httpx.Response(304)]
    )
    await retry_client.extras.color_families(etag='"abc"')
    assert route.call_count == 3
    assert all(call.request.headers["if-none-match"] == '"abc"' for call in route.calls)


@pytest.mark.asyncio
async def test_honours_retry_after_seconds(retry_client, mock_api, sleeps):
    mock_api.get("/color_families.json").mock(
        side_effect=[httpx.Response(429, headers={"Retry-After": "7"}), httpx.Response(200, json={})]
    )
    await retry_client.extras.color_families()
    assert sleeps == [7.0]


@pytest.mark.asyncio
async def test_retry_after_is_capped(retry_client, mock_api, sleeps):
    mock_api.get("/color_families.json").mock(
        side_effect=[httpx.Response(503, headers={"Retry-After": "3600"}), httpx.Response(200, json={})]
    )
    await retry_client.extras.color_families()
    assert sleeps == [_retry.MAX_DELAY]


@pytest.mark.asyncio
async def test_backoff_grows_exponentially(retry_client, mock_api, sleeps):
    mock_api.get("/color_families.json").respond(502)
    with pytest.raises(RavelryAPIError):
        await retry_client.extras.color_families()
    first, second = sleeps
    assert 0.25 <= first <= 0.5
    assert 0.5 <= second <= 1.0


@pytest.mark.asyncio
async def test_oauth_client_supports_retries(mock_api, sleeps):
    route = mock_api.get("/current_user.json").mock(
        side_effect=[httpx.ConnectError("x"), httpx.Response(200, json={"user": {}})]
    )
    c = RavelryClient.from_oauth_token("tok", max_retries=1)
    await c.people.me()
    assert route.call_count == 2
    assert all(call.request.headers["authorization"] == "Bearer tok" for call in route.calls)
    await c.aclose()


def test_negative_max_retries_rejected():
    with pytest.raises(ValueError, match="max_retries"):
        RavelryClient(username="u", api_key="k", max_retries=-1)
    with pytest.raises(ValueError, match="max_retries"):
        RavelryClient.from_oauth_token("tok", max_retries=-1)


class TestRetryAfterParsing:
    def _resp(self, value=None):
        headers = {"Retry-After": value} if value is not None else {}
        return httpx.Response(503, headers=headers)

    def test_missing(self):
        assert _retry._retry_after(self._resp()) is None

    def test_seconds(self):
        assert _retry._retry_after(self._resp(" 3 ")) == 3.0

    def test_http_date(self):
        future = email.utils.formatdate(time.time() + 10, usegmt=True)
        assert 8.0 <= _retry._retry_after(self._resp(future)) <= 10.0

    def test_http_date_in_past_is_zero(self):
        past = email.utils.formatdate(time.time() - 60, usegmt=True)
        assert _retry._retry_after(self._resp(past)) == 0.0

    def test_garbage_ignored(self):
        assert _retry._retry_after(self._resp("soon")) is None


class TestBackoff:
    def test_capped(self):
        assert _retry._backoff(100) <= _retry.MAX_DELAY

    def test_jitter_range(self):
        for attempt in range(4):
            nominal = _retry.BACKOFF_BASE * 2**attempt
            assert nominal * 0.5 <= _retry._backoff(attempt) <= nominal
