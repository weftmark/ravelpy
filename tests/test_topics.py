"""Tests for :class:`~ravelpy.resources.topics.Topics` resource methods."""


def test_show_topic(client, mock_api):
    mock_api.get("/topics/20.json").respond(200, json={"topic": {"id": 20}})
    _, _, raw = client.topics.show(topic_id=20)
    assert raw["topic"]["id"] == 20


def test_topic_posts(client, mock_api):
    mock_api.get("/topics/20/posts.json").respond(200, json={"forum_posts": []})
    client.topics.posts(topic_id=20)


def test_topic_posts_pagination(client, mock_api):
    mock_api.get("/topics/20/posts.json").respond(200, json={"forum_posts": []})
    client.topics.posts(topic_id=20, page=3, page_size=25)
    url = str(mock_api.calls.last.request.url)
    assert "page=3" in url
