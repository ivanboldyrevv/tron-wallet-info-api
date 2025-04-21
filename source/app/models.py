from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float

from app.database import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class WalletQuery(BaseModel):
    __tablename__ = "wallet_queries"

    address = Column(String, index=True)
    bandwidth = Column(Integer)
    energy = Column(Integer)
    balance = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
