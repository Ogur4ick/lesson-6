from operator import attrgetter
from typing import Literal
from .repository import OrderRepository
from .schemas import Order, OrderCreate, OrderUpdate, OrderStatus
from .exceptions import OrderNotFoundError, OrderAlreadyCompletedError

SortField = Literal["created_at", "drink"]

class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, payload: OrderCreate) -> Order:
        return self.repository.add(Order(id=self.repository.allocate_id(), **payload.model_dump()))

    def get_order(self, order_id: int) -> Order:
        result = self.repository.get_by_id(order_id)
        if result is None:
            raise OrderNotFoundError(order_id)
        return result

    def list_orders(self, status: OrderStatus | None = None, limit: int | None = None,
                    offset: int = 0, sort_by: SortField = "created_at") -> list[Order]:
        selected = [item for item in self.repository.get_all() if status is None or item.status == status]
        selected = sorted(selected, key=attrgetter(sort_by))
        end = None if limit is None else offset + limit
        return selected[offset:end]

    def count_orders(self) -> int:
        return len(self.repository.get_all())

    def _require_mutable(self, order_id: int) -> None:
        if self.get_order(order_id).status == OrderStatus.completed:
            raise OrderAlreadyCompletedError(order_id)

    def update_order(self, order_id: int, payload: OrderUpdate) -> Order:
        self._require_mutable(order_id)
        changes = payload.model_dump(exclude_unset=True, exclude_none=True)
        result = self.repository.update(order_id, changes)
        if result is None:
            raise OrderNotFoundError(order_id)
        return result

    def cancel_order(self, order_id: int) -> None:
        self._require_mutable(order_id)
        if not self.repository.delete(order_id):
            raise OrderNotFoundError(order_id)
