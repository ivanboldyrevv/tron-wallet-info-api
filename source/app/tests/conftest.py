# tests/conftest.py
import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import create_app
from app.container import Container
from app.models import Base


conf = {
    "tron": {
        "address": "TJ9Mk7TAuP8AyDwjU3Hjimo7GCyuRMoVcK",
        "network": "https://api.shasta.trongrid.io"
    },
    "database": {
        "uri": "postgresql+asyncpg://admin:admin@postgres:5432/test_db"
    }
}


@pytest.fixture
def test_network():
    return conf["tron"]["network"]


@pytest.fixture
def test_address():
    return conf["tron"]["address"]


@pytest.fixture
def db_uri():
    return conf["database"]["uri"]


@pytest.fixture
def wallet_data():
    return {"wallet_address": conf["tron"]["address"]}


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("postgresql+psycopg2://admin:admin@postgres:5432/test_db", echo=True)
    session = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)
    yield session
    Base.metadata.drop_all(engine)


@pytest_asyncio.fixture(scope="function")
async def client():
    c = Container()
    c.config.from_dict(conf)

    app = create_app(c)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
