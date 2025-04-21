from dependency_injector import containers, providers

from app.database import AsyncDatabase
from app.services.tron_service import TronInfoService
from app.services.wallet_query_service import WalletQueryService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app.routes"])
    config = providers.Configuration()

    db = providers.Singleton(
        AsyncDatabase,
        db_uri=config.database.uri)

    api_service = providers.Factory(
        TronInfoService,
        network=config.tron.network)

    query_service = providers.Factory(
        WalletQueryService,
        factory_session=db.provided.session)
