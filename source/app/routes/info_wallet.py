from pydantic import PositiveInt
from fastapi import APIRouter, Depends, HTTPException, status
from dependency_injector.wiring import Provide, inject

from typing import Annotated

from app.schema.info_wallet_response import (WalletMetrics,
                                             PaginatedWalletQueries)
from app.schema.info_wallet_request import InfoWalletRequest

from app.container import Container
from app.services.tron_service import TronInfoService
from app.services.wallet_query_service import WalletQueryService

from app.exceptions import NotFoundException


info_wallet = APIRouter(
    prefix="/wallet_info"
)


@info_wallet.post(
        path="",
        response_model=WalletMetrics,
        status_code=status.HTTP_201_CREATED
)
@inject
async def get_wallet_info(
    address: InfoWalletRequest,
    api_service: Annotated[TronInfoService, Depends(Provide[Container.api_service])],
    query_service: Annotated[WalletQueryService, Depends(Provide[Container.query_service])]
) -> WalletMetrics:
    try:
        response = await api_service.get_resources(addr=address.wallet_address)

        entity = await query_service.insert_wallet_access(
            addr=address.wallet_address,
            bandwidth=response["bandwidth"],
            energy=response["energy"],
            balance=float(response["balance"]))

        return entity
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process wallet metrics. "
                   "Please, check wallet address!"
        )


@info_wallet.get(
        path="",
        response_model=PaginatedWalletQueries
)
@inject
async def get_wallet_queries(
    query_service: Annotated[WalletQueryService, Depends(Provide[Container.query_service])],
    page: PositiveInt,
    per_page: PositiveInt = 10
) -> PaginatedWalletQueries:
    try:
        total = await query_service.total_counts()
        total_pages = (total + per_page - 1) // per_page

        queries = await query_service.select_wallet_queries(page=page, per_page=per_page)

        return {
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages if total_pages > 0 else 1,
            "total_items": total,
            "items": queries
        }
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.msg
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve query history: {str(e)}"
        )
