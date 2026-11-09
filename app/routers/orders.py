from fastapi import APIRouter, Response
from ..dependencies import ServiceDep, PaginationDep
from ..schemas import Order, OrderCreate, OrderUpdate, OrderStatus
from ..service import SortField

router = APIRouter(prefix="/orders", tags=["Заказы"])

@router.post("", status_code=201, response_model=Order, summary="Создать заказ")
async def create_order(payload: OrderCreate, service: ServiceDep):
    return service.create_order(payload)

@router.get("", response_model=list[Order], summary="Получить список заказов")
async def list_orders(service: ServiceDep, pagination: PaginationDep,
                      status: OrderStatus | None = None, sort_by: SortField = "created_at"):
    return service.list_orders(status=status, limit=pagination.limit, offset=pagination.offset, sort_by=sort_by)

@router.get("/{order_id}", response_model=Order, summary="Получить заказ по идентификатору")
async def get_order(order_id: int, service: ServiceDep):
    return service.get_order(order_id)

@router.patch("/{order_id}", response_model=Order, summary="Частично обновить заказ")
async def update_order(order_id: int, payload: OrderUpdate, service: ServiceDep):
    return service.update_order(order_id, payload)

@router.delete("/{order_id}", status_code=204, response_class=Response, summary="Отменить заказ")
async def cancel_order(order_id: int, service: ServiceDep):
    service.cancel_order(order_id)
    return Response(status_code=204)
