"""Tests for :class:`~ravelpy.resources.messages.Messages` resource methods."""

import pytest


@pytest.mark.asyncio
async def test_list_messages(client, mock_api):
    mock_api.get("/messages/list.json").respond(200, json={"messages": []})
    await client.messages.list()


@pytest.mark.asyncio
async def test_list_messages_pagination(client, mock_api):
    mock_api.get("/messages/list.json").respond(200, json={"messages": []})
    await client.messages.list(page=2, page_size=10)
    url = str(mock_api.calls.last.request.url)
    assert "page=2" in url


@pytest.mark.asyncio
async def test_show_message(client, mock_api):
    mock_api.get("/messages/11.json").respond(200, json={"message": {"id": 11}})
    _, _, raw = await client.messages.show(message_id=11)
    assert raw["message"]["id"] == 11
