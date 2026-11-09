from dataclasses import dataclass
from functools import lru_cache
from typing import Annotated
from fastapi import Depends, Query, HTTPException
from .config import Settings, get_settings
from .repository import OrderRepository
from .service import OrderService

SettingsDep = Annotated[Settings, Depends(get_settings)]

@lru_cache
def get_repository() -> OrderRepository:
    return OrderRepository()

def get_service(repository: Annotated[OrderRepository, Depends(get_repository)]) -> OrderService:
    return OrderService(repository)

ServiceDep = Annotated[OrderService, Depends(get_service)]

@dataclass(frozen=True)
class Pagination:
    limit: int
    offset: int

def pagination_params(
    settings: SettingsDep,
    limit: Annotated[int | None, Query(ge=1, description="Число записей; значение по умолчанию из настроек")] = None,
    offset: Annotated[int | None, Query(ge=0, description="Смещение; значение по умолчанию из настроек")] = None,
) -> Pagination:
    page_size = settings.default_page_size if limit is None else limit
    if page_size > settings.max_page_size:
        raise HTTPException(422, detail=f"Максимальное значение limit: {settings.max_page_size}")
    return Pagination(page_size, settings.default_offset if offset is None else offset)

PaginationDep = Annotated[Pagination, Depends(pagination_params)]
