"""Tests for :class:`~ravelpy.resources.shops.Shops` resource methods."""


def test_search_shops(client, mock_api):
    mock_api.get("/shops/search.json").respond(200, json={"shops": []})
    client.shops.search(query="wool")
    assert "query=wool" in str(mock_api.calls.last.request.url)


def test_show_shop(client, mock_api):
    mock_api.get("/shops/8.json").respond(200, json={"shop": {"id": 8}})
    _, _, raw = client.shops.show(shop_id=8)
    assert raw["shop"]["id"] == 8
