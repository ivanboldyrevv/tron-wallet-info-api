import pytest
from unittest.mock import MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.wallet_query_service import WalletQueryService
from app.models import WalletQuery
from app.exceptions import PageIndexException


@pytest.fixture
def mock_factory_session():
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.commit = AsyncMock()
    mock_session.rollback = AsyncMock()
    mock_session.execute = AsyncMock()
    mock_session.scalar = AsyncMock()

    mock_context_manager = AsyncMock()
    mock_context_manager.__aenter__.return_value = mock_session
    mock_context_manager.__aexit__.return_value = None

    def factory():
        return mock_context_manager

    return factory


@pytest.fixture
def service(mock_factory_session):
    return WalletQueryService(factory_session=mock_factory_session)


@pytest.mark.asyncio
async def test_insert_wallet_access(service):
    new_entity = await service.insert_wallet_access(
        addr="TABCDEF",
        bandwidth=1000,
        energy=500,
        balance=1000.0
    )

    assert isinstance(new_entity, WalletQuery)
    assert new_entity.address == "TABCDEF"
    assert new_entity.bandwidth == 1000
    assert new_entity.energy == 500
    assert new_entity.balance == 1000.0


@pytest.mark.asyncio
async def test_insert_wallet_access_raises_and_rolls_back(mock_factory_session):
    svc = WalletQueryService(factory_session=mock_factory_session)
    mock_session = await mock_factory_session().__aenter__()

    mock_session.commit.side_effect = Exception("DB error")

    with pytest.raises(Exception, match="DB error"):
        await svc.insert_wallet_access(
            addr="T_FAIL",
            bandwidth=0,
            energy=0,
            balance=0.0
        )

    mock_session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_select_wallet_queries_with_data(service, mock_factory_session):
    mock_session = await mock_factory_session().__aenter__()

    mock_execute_result = MagicMock()
    mock_execute_result.scalars.return_value.all.return_value = [
        WalletQuery(id=1, address="ADDR1"),
        WalletQuery(id=2, address="ADDR2")
    ]

    mock_session.execute.return_value = mock_execute_result

    result = await service.select_wallet_queries(page=1, per_page=10)

    assert len(result) == 2
    assert result[0].address == "ADDR1"


@pytest.mark.asyncio
async def test_select_wallet_queries_without_data(service, mock_factory_session):
    mock_session = await mock_factory_session().__aenter__()

    mock_execute_result = MagicMock()
    mock_execute_result.scalars.return_value.all.return_value = []

    mock_session.execute.return_value = mock_execute_result

    with pytest.raises(PageIndexException):
        await service.select_wallet_queries(page=1, per_page=10)


@pytest.mark.asyncio
async def test_get_total(service, mock_factory_session):
    mock_session = await mock_factory_session().__aenter__()

    mock_session.scalar.return_value = 2

    result = await service.total_counts()
    assert result == 2
