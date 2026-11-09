from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class DrinkSize(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"

class OrderStatus(str, Enum):
    pending = "pending"
    ready = "ready"
    completed = "completed"

class OrderCreate(BaseModel):
    drink: str = Field(min_length=1, description="Название напитка из меню", examples=["Латте"])
    size: DrinkSize = Field(description="Размер напитка", examples=["medium"])
    quantity: int = Field(gt=0, description="Количество напитков", examples=[2])
    customer_name: str | None = Field(None, description="Имя клиента", examples=["Ирина"])

class OrderUpdate(BaseModel):
    drink: str | None = Field(None, min_length=1, description="Название напитка", examples=["Какао"])
    size: DrinkSize | None = Field(None, description="Размер напитка")
    quantity: int | None = Field(None, gt=0, description="Количество напитков")
    customer_name: str | None = Field(None, description="Имя клиента")
    status: OrderStatus | None = Field(None, description="Новый статус заказа")

class Order(OrderCreate):
    id: int = Field(description="Номер заказа")
    status: OrderStatus = Field(default=OrderStatus.pending, description="Состояние заказа")
    created_at: datetime = Field(default_factory=datetime.now, description="Дата и время создания")
