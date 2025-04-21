from fastapi import FastAPI

from typing import Optional

from app.container import Container
from app.routes.info_wallet import info_wallet


def create_app(container: Optional[Container] = None) -> FastAPI:
    if container is None:
        container = Container()
        container.config.from_yaml("./app/config.yml")

    app = FastAPI(
        title="Tron network wallet's info"
    )

    app.container = container
    app.include_router(info_wallet)

    return app


app = create_app()
