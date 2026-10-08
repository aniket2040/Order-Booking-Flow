from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies.service import (
    get_order_service,
)
from app.Services.order.order_service import (
    OrderService,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)

@router.get(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
)
async def get_order(
    order_id: UUID,
    order_service: OrderService = Depends(
        get_order_service,
    ),
):
    """
    Retrieve an order by ID.
    """

    order = await order_service.get_order(
        order_id
    )

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found.",
        )

    return order


@router.get(
    "/customer/{customer_id}",
    status_code=status.HTTP_200_OK,
)
async def get_customer_orders(
    customer_id: UUID,
    order_service: OrderService = Depends(
        get_order_service,
    ),
):
    """
    Retrieve all customer orders.
    """

    return await order_service.get_customer_orders(
        customer_id
    )