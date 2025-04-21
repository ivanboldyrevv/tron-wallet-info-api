import pytest
from app.services.tron_service import TronInfoService


@pytest.fixture
def service(test_network):
    service = TronInfoService(test_network)
    return service


@pytest.mark.asyncio
async def test_get_resources(service, test_address):
    result = await service.get_resources(test_address)

    assert result["energy"] == 0
    assert result["bandwidth"] == 600
    assert float(result["balance"]) == 2000


@pytest.mark.asyncio
async def test_get_energy(service, test_address):
    result = await service.get_energy(test_address)
    assert result == 0


@pytest.mark.asyncio
async def test_get_bandwidth(service, test_address):
    result = await service.get_bandwidth(test_address)
    assert result == 600


@pytest.mark.asyncio
async def test_get_balance(service, test_address):
    result = await service.get_balance(test_address)
    assert result == 2000


@pytest.mark.asyncio
async def test_get_account_net(service, test_address):
    result = await service.get_account_net(test_address)
    assert all(key in result for key in ["freeNetLimit", "TotalNetLimit", "TotalNetWeight"])


@pytest.mark.asyncio
async def test_get_account(service, test_address):
    result = await service.get_account(test_address)

    assert result["address"] == test_address
    assert result["balance"] == 2_000_000_000
