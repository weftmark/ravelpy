def test_show_fiber(client, mock_api):
    mock_api.get("/people/foo/fiber/4.json").respond(200, json={"fiber": {"id": 4}})
    _, _, raw = client.fiber.show(username="foo", fiber_id=4)
    assert raw["fiber"]["id"] == 4


def test_fiber_comments(client, mock_api):
    mock_api.get("/people/foo/fiber/4/comments.json").respond(200, json={"comments": []})
    client.fiber.comments(username="foo", fiber_id=4)


def test_fiber_comments_pagination(client, mock_api):
    mock_api.get("/people/foo/fiber/4/comments.json").respond(200, json={"comments": []})
    client.fiber.comments(username="foo", fiber_id=4, page=2, page_size=10, sort="date")
    url = str(mock_api.calls.last.request.url)
    assert "page=2" in url
    assert "sort=date" in url
