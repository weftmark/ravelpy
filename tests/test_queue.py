"""Tests for :class:`~ravelpy.resources.queue.Queue` resource methods."""


def test_list_queue(client, mock_api):
    mock_api.get("/people/foo/queue/list.json").respond(200, json={"queued_projects": []})
    client.queue.list(username="foo")


def test_list_queue_pagination(client, mock_api):
    mock_api.get("/people/foo/queue/list.json").respond(200, json={"queued_projects": []})
    client.queue.list(username="foo", page=2, page_size=10)
    url = str(mock_api.calls.last.request.url)
    assert "page=2" in url


def test_show_queue_item(client, mock_api):
    mock_api.get("/people/foo/queue/5.json").respond(200, json={"queued_project": {"id": 5}})
    _, _, raw = client.queue.show(username="foo", queue_id=5)
    assert raw["queued_project"]["id"] == 5
