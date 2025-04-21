from pydantic import BaseModel, Field


class InfoWalletRequest(BaseModel):
    wallet_address: str = Field(..., description="Wallet address",
                                json_schema_extra={"example": "TXYZ..."})
