"""Caller-supplied path arguments are percent-encoded into a single URL segment (#43)."""

import pytest

from ravelpy.resources.base import Resource

HOSTILE = "../x?y#z"
HOSTILE_ENCODED = "..%2Fx%3Fy%23z"


def _raw_path(mock_api) -> str:
    """Return the request path exactly as httpx would send it on the wire."""
    return mock_api.calls.last.request.url.raw_path.decode("ascii")


def test_path_helper_encodes_each_segment():
    assert Resource._path("/people/{}/stash/{}.json", HOSTILE, 7) == f"/people/{HOSTILE_ENCODED}/stash/7.json"


def test_path_helper_keeps_legitimate_values_unchanged():
    assert Resource._path("/projects/{}/{}.json", "Foo-bar_1.x", 42) == "/projects/Foo-bar_1.x/42.json"


@pytest.mark.asyncio
async def test_get_with_hostile_username_stays_on_endpoint(client, mock_api):
    mock_api.route().respond(200, json={"user": {}})
    await client.people.show(username=HOSTILE)
    request = mock_api.calls.last.request
    assert _raw_path(mock_api) == f"/people/{HOSTILE_ENCODED}.json"
    assert request.url.query == b""
    assert request.url.fragment == ""


@pytest.mark.asyncio
async def test_get_cannot_reach_other_endpoint_via_dot_segments(client, mock_api):
    mock_api.route().respond(200, json={})
    await client.stash.list(username="../messages/list.json?")
    assert _raw_path(mock_api) == "/people/..%2Fmessages%2Flist.json%3F/stash/list.json"


@pytest.mark.parametrize(("value", "encoded"), [("..", "%2E%2E"), (".", "%2E")])
def test_path_helper_encodes_dot_segments(value, encoded):
    assert Resource._path("/people/{}/stash/list.json", value) == f"/people/{encoded}/stash/list.json"


@pytest.mark.asyncio
@pytest.mark.parametrize(("value", "encoded"), [("..", "%2E%2E"), (".", "%2E")])
async def test_whole_segment_dots_are_not_collapsed(client, mock_api, value, encoded):
    mock_api.route().respond(200, json={})
    await client.stash.list(username=value)
    # Without encoding, "/people/../stash/list.json" would collapse to "/stash/list.json".
    assert _raw_path(mock_api) == f"/people/{encoded}/stash/list.json"


@pytest.mark.asyncio
async def test_string_id_is_encoded(client, mock_api):
    mock_api.route().respond(200, json={})
    await client.patterns.show(pattern_id="1/../../current_user")
    assert _raw_path(mock_api) == "/patterns/1%2F..%2F..%2Fcurrent_user.json"


@pytest.mark.asyncio
async def test_post_with_hostile_username_stays_on_endpoint(client, mock_api):
    mock_api.route().respond(200, json={"stash": {"id": 1}})
    await client.stash.create(HOSTILE, {"yarn_id": 1})
    request = mock_api.calls.last.request
    assert request.method == "POST"
    assert _raw_path(mock_api) == f"/people/{HOSTILE_ENCODED}/stash/create.json"
    assert request.url.query == b""


@pytest.mark.asyncio
async def test_post_cannot_be_retargeted(client, mock_api):
    mock_api.route().respond(200, json={})
    await client.stash.create("a/../../x?", {})
    assert _raw_path(mock_api) == "/people/a%2F..%2F..%2Fx%3F/stash/create.json"


@pytest.mark.asyncio
async def test_legitimate_values_produce_identical_urls(client, mock_api):
    mock_api.route().respond(200, json={})
    await client.projects.show(username="Knit-ter_1.0", project_id=123)
    assert str(mock_api.calls.last.request.url) == "https://api.ravelry.com/projects/Knit-ter_1.0/123.json"
    await client.stash.create("you", {})
    assert str(mock_api.calls.last.request.url) == "https://api.ravelry.com/people/you/stash/create.json"
