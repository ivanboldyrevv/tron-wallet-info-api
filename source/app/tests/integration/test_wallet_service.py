import pytest

from app.database import AsyncDatabase
from app.models import WalletQuery
from app.services.wallet_query_service import WalletQueryService
from app.exceptions import NotFoundException


@pytest.fixture
def service(db_uri):
    db = AsyncDatabase(db_uri)
    service = WalletQueryService(db.session)
    return service


@pytest.mark.asyncio
async def test_insertWalletAccess_expectedEntity(service, db_session):
    expected_entity = {
        "addr": "test_addr",
        "bandwidth": 100,
        "energy": 100,
        "balance": 100.0
    }

    result = await service.insert_wallet_access(**expected_entity)

    assert result.address == expected_entity["addr"]
    assert result.bandwidth == expected_entity["bandwidth"]
    assert result.energy == expected_entity["energy"]
    assert result.balance == expected_entity["balance"]


@pytest.mark.asyncio
async def test_insertWalletAccess_expectedDatabaseRow(service, db_session):
    entity = {
        "addr": "test_addr",
        "bandwidth": 100,
        "energy": 100,
        "balance": 100.0
    }

    result = await service.insert_wallet_access(**entity)

    with db_session() as sess:
        res = sess.query(WalletQuery).first()

        assert result.address == res.address
        assert result.bandwidth == res.bandwidth
        assert result.energy == res.energy
        assert result.balance == res.balance
        assert result.created_at == res.created_at


@pytest.mark.asyncio
async def test_selectWalletQueries_expectedEntity(service, db_session):
    expected_params = {
        "address": "test_address",
        "bandwidth": 100,
        "energy": 100,
        "balance": 100.0
    }

    with db_session() as sess:
        sess.add(WalletQuery(**expected_params))
        sess.commit()

    result = await service.select_wallet_queries(1, 10)

    assert result[0].address == expected_params["address"]
    assert result[0].bandwidth == expected_params["bandwidth"]
    assert result[0].energy == expected_params["energy"]
    assert result[0].balance == expected_params["balance"]


@pytest.mark.asyncio
async def test_selectWalletQueries_raiseException(service, db_session):
    with pytest.raises(NotFoundException):
        await service.select_wallet_queries(100, 100)


@pytest.mark.asyncio
async def test_totalCount_expectedCount(service, db_session):
    params = {
        "address": "test_address",
        "bandwidth": 100,
        "energy": 100,
        "balance": 100.0
    }

    with db_session() as sess:
        sess.add(WalletQuery(**params))
        sess.commit()

    result = await service.total_counts()
    assert result == 1


@pytest.mark.asyncio
async def test_totalCount_raiseValueError(service, db_session):
    with pytest.raises(ValueError):
        await service.total_counts()
