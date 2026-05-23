"""Tests for :class:`~ravelpy.resources.products.Products` resource methods."""

import pytest


@pytest.mark.asyncio
async def test_show_product(client, mock_api):
    mock_api.get("/products/15.json").respond(200, json={"product": {"id": 15}})
    _, _, raw = await client.products.show(product_id=15)
    assert raw["product"]["id"] == 15


@pytest.mark.asyncio
async def test_product_attachments(client, mock_api):
    mock_api.get("/products/15/attachments.json").respond(200, json={"product_attachments": []})
    await client.products.attachments(product_id=15)


@pytest.mark.asyncio
async def test_show_product_attachment(client, mock_api):
    mock_api.get("/product_attachments/3.json").respond(200, json={"product_attachment": {"id": 3}})
    _, _, raw = await client.product_attachments.show(attachment_id=3)
    assert raw["product_attachment"]["id"] == 3
