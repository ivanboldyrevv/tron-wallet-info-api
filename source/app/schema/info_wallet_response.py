from datetime import datetime
from pydantic import BaseModel, Field, PositiveInt
from typing import List


class WalletMetrics(BaseModel):
    bandwidth: int = Field(..., description="Bandwidth in bytes")
    energy: int = Field(..., description="Energy TRX")
    balance: float = Field(..., description="Balance in TRX",
                           json_schema_extra={"example": 123.45})


class WalletQueryResponse(WalletMetrics):
    address: str = Field(..., description="Wallet address",
                         json_schema_extra={"example": "TXYZ..."})
    created_at: datetime = Field(..., description="Record time creation")


class PaginatedWalletQueries(BaseModel):
    page: PositiveInt = Field(..., description="Current page",
                              json_schema_extra={"example": 1})
    per_page: PositiveInt = Field(..., description="Elements per page",
                                  json_schema_extra={"example": 10})
    total_pages: PositiveInt = Field(..., description="Total pages",
                                     json_schema_extra={"example": 100})
    items: List[WalletQueryResponse] = Field(..., description="Wallets ordered by descending")
