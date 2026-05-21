def test_list_messages(client, mock_api):
    mock_api.get("/messages/list.json").respond(200, json={"messages": []})
    client.messages.list()


def test_list_messages_pagination(client, mock_api):
    mock_api.get("/messages/list.json").respond(200, json={"messages": []})
    client.messages.list(page=2, page_size=10)
    url = str(mock_api.calls.last.request.url)
    assert "page=2" in url


def test_show_message(client, mock_api):
    mock_api.get("/messages/11.json").respond(200, json={"message": {"id": 11}})
    _, _, raw = client.messages.show(message_id=11)
    assert raw["message"]["id"] == 11
