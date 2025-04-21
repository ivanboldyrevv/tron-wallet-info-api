import pytest
from unittest.mock import AsyncMock
from app.services.tron_service import TronInfoService


@pytest.fixture
def service():
    service = TronInfoService(network="mock")

    service.get_account_net = AsyncMock()
    service.get_account_net.return_value = {
        "freeNetLimit": 50,
        "freeNetUsed": 50,
        "NetLimit": 50,
        "NetUsed": 10,
        "EnergyLimit": 100,
        "EnergyUsed": 50
    }

    service.get_account = AsyncMock()
    service.get_account.return_value = {
        "balance": 1_000_000
    }

    return service


@pytest.mark.asyncio
async def test_get_energy(service):
    result = await service.get_energy(addr="mock_addr")

    # 100 (EnergyLimit) - 50 (EnergyUsed) = 50
    assert result == 50
    service.get_account_net.assert_awaited_once_with("mock_addr")


@pytest.mark.asyncio
async def test_get_bandwidth(service):
    result = await service.get_bandwidth(addr="mock_addr")

    # (50-50) + (50-10) = 0 + 40 = 40
    assert result == 40
    service.get_account_net.assert_awaited_once_with("mock_addr")


@pytest.mark.asyncio
async def test_get_balance(service):
    result = await service.get_balance(addr="mock_addr")

    # 1_000_000 / 1_000_000 = 1.0
    assert result == 1.0
    service.get_account.assert_awaited_once_with("mock_addr")
