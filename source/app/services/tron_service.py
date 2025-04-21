import httpx
from httpx import Response
from typing import Dict, Any, Optional


class TronInfoService:
    def __init__(self, network: str) -> None:
        self.network = network

        self.headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

    async def get_resources(self, addr: str) -> Dict[str, Any]:
        return {
            "bandwidth": await self.get_bandwidth(addr),
            "energy": await self.get_energy(addr),
            "balance": f"{await self.get_balance(addr):.2f}"
        }

    async def get_energy(self, addr: str) -> int:
        content = await self.get_account_net(addr)
        return content.get("EnergyLimit", 0) - content.get("EnergyUsed", 0)

    async def get_bandwidth(self, addr: str) -> int:
        content = await self.get_account_net(addr)
        return (content["freeNetLimit"]
                - content.get("freeNetUsed", 0)
                + content.get("NetLimit", 0)
                - content.get("NetUsed", 0))

    async def get_balance(self, addr: str) -> float:
        content = await self.get_account(addr)
        return content.get("balance", 0) / 1_000_000

    async def get_account_net(self, addr: str):
        response = await self._make_request(
            endpoint="wallet/getaccountnet",
            payload={"address": addr, "visible": True})
        return response.json()

    async def get_account(self, addr: str) -> Dict[str, Any]:
        response = await self._make_request(
            endpoint="wallet/getaccount",
            payload={"address": addr, "visible": True})
        return response.json()

    async def _make_request(
            self,
            endpoint: str,
            payload: Dict[str, Any],
            headers: Optional[Dict[str, Any]] = None) -> Response:

        headers = headers or self.headers

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f"{self.network}/{endpoint}",
                json=payload,
                headers=headers)
            response.raise_for_status()
        return response
