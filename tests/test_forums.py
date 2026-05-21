def test_forum_sets(client, mock_api):
    mock_api.get("/forums/sets.json").respond(200, json={"forum_sets": []})
    client.forums.sets()


def test_forum_topics(client, mock_api):
    mock_api.get("/forums/1/topics.json").respond(200, json={"topics": []})
    client.forums.topics(forum_id=1)


def test_forum_topics_pagination(client, mock_api):
    mock_api.get("/forums/1/topics.json").respond(200, json={"topics": []})
    client.forums.topics(forum_id=1, page=2, page_size=25)
    url = str(mock_api.calls.last.request.url)
    assert "page=2" in url


def test_filtered_topics(client, mock_api):
    mock_api.get("/forums/filtered_topics.json").respond(200, json={"topics": []})
    client.forums.filtered_topics()


def test_forum_post(client, mock_api):
    mock_api.get("/forum_posts/99.json").respond(200, json={"forum_post": {"id": 99}})
    _, _, raw = client.forums.post(post_id=99)
    assert raw["forum_post"]["id"] == 99


def test_unread_forum_posts(client, mock_api):
    mock_api.get("/forum_posts/unread.json").respond(200, json={"forum_posts": []})
    client.forums.unread_posts()
