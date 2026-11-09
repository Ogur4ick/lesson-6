from typing import Any
from .schemas import Order

class OrderRepository:
    def __init__(self):
        self._orders: list[Order] = []
        self._sequence = 0

    def allocate_id(self) -> int:
        self._sequence += 1
        return self._sequence

    def _position(self, order_id: int) -> int | None:
        return next((index for index, item in enumerate(self._orders) if item.id == order_id), None)

    def get_all(self) -> list[Order]:
        return [item.model_copy(deep=True) for item in self._orders]

    def get_by_id(self, order_id: int) -> Order | None:
        position = self._position(order_id)
        return None if position is None else self._orders[position].model_copy(deep=True)

    def add(self, order: Order) -> Order:
        self._orders.append(order.model_copy(deep=True))
        self._sequence = max(self._sequence, order.id)
        return order.model_copy(deep=True)

    def update(self, order_id: int, update_data: dict[str, Any]) -> Order | None:
        position = self._position(order_id)
        if position is None:
            return None
        values = self._orders[position].model_dump()
        values.update(update_data)
        self._orders[position] = Order.model_validate(values)
        return self._orders[position].model_copy(deep=True)

    def delete(self, order_id: int) -> bool:
        position = self._position(order_id)
        if position is None:
            return False
        del self._orders[position]
        return True
