from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .config import get_settings
from .dependencies import ServiceDep, SettingsDep
from .exceptions import OrderNotFoundError, OrderAlreadyCompletedError
from .routers import orders

app = FastAPI(title=get_settings().app_name,
              description="Приложение для регистрации и обработки заказов кофейни.",
              version="1.0.0",
              openapi_tags=[{"name": "Заказы"}, {"name": "Сервис"}])
app.include_router(orders.router)

@app.exception_handler(OrderNotFoundError)
async def handle_missing(request: Request, error: OrderNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(error)})

@app.exception_handler(OrderAlreadyCompletedError)
async def handle_completed(request: Request, error: OrderAlreadyCompletedError):
    return JSONResponse(status_code=409, content={"detail": str(error)})

@app.get("/", tags=["Сервис"], summary="Приветствие сервиса")
async def welcome(settings: SettingsDep):
    return {"message": f"Добро пожаловать в сервис «{settings.app_name}»!"}

@app.get("/info", tags=["Сервис"], summary="Информация о сервисе")
async def application_info(settings: SettingsDep, service: ServiceDep):
    return {"app_name": settings.app_name, "orders_count": service.count_orders()}
