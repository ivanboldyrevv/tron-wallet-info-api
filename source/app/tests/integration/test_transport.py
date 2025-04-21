import pytest


def response_ok(response):
    content = response.json()
    expected_response = {
        "bandwidth": 600,
        "energy": 0,
        "balance": 2000
    }

    assert response.status_code == 201
    assert isinstance(content, dict)
    assert all(key in content for key in ["bandwidth", "energy", "balance"])
    assert content == expected_response


@pytest.mark.asyncio
async def test_get_wallet_info(client, wallet_data, db_session):
    response = await client.post("/wallet_info", json=wallet_data)
    response_ok(response)


@pytest.mark.asyncio
async def test_get_wallet_queries(client, wallet_data, db_session):
    post_response = await client.post("/wallet_info", json=wallet_data)
    response_ok(post_response)

    response = await client.get("/wallet_info", params={"page": 1})
    content = response.json()

    assert response.status_code == 200
    assert content["page"] == 1
    assert content["per_page"] == 10
    assert content["total_pages"] == 1

    queries = content["items"]
    assert isinstance(queries, list) is True
    assert len(queries) > 0


@pytest.mark.asyncio
async def test_get_wallet_queries_raise_on_wrong_page(client, wallet_data, db_session):
    post_response = await client.post("/wallet_info", json=wallet_data)
    response_ok(post_response)

    response = await client.get("/wallet_info", params={"page": 0})
    assert response.status_code == 422

    response = await client.get("/wallet_info", params={"page": -1})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_wallet_queries_raise_on_wrong_per_page(client, wallet_data, db_session):
    post_response = await client.post("/wallet_info", json=wallet_data)
    response_ok(post_response)

    response = await client.get("/wallet_info", params={"page": 1, "per_page": 0})
    assert response.status_code == 422

    response = await client.get("/wallet_info", params={"page": 1, "per_page": -1})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_wallet_queries_raise_pagination_error(client, wallet_data, db_session):
    post_response = await client.post("/wallet_info", json=wallet_data)
    response_ok(post_response)

    response = await client.get("/wallet_info", params={"page": 100})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_wallet_queries_raise_value_error(client, db_session):
    response = await client.get("/wallet_info", params={"page": 100})
    assert response.status_code == 500
