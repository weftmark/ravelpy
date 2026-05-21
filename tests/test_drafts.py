def test_list_drafts(client, mock_api):
    mock_api.get("/drafts/patterns/list.json").respond(200, json={"draft_patterns": []})
    client.drafts.list()


def test_list_drafts_with_business_id(client, mock_api):
    mock_api.get("/drafts/patterns/list.json").respond(200, json={"draft_patterns": []})
    client.drafts.list(business_id=5)
    assert "business_id=5" in str(mock_api.calls.last.request.url)


def test_show_draft(client, mock_api):
    mock_api.get("/drafts/patterns/99.json").respond(200, json={"draft_pattern": {"id": 99}})
    _, _, raw = client.drafts.show(pattern_id=99)
    assert raw["draft_pattern"]["id"] == 99
