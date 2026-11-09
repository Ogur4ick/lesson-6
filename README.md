# Учёт заказов

## Запуск

Python 3.10 или новее. Из корня проекта:

```bash
python -m venv .venv
```

Активируйте окружение: `source .venv/bin/activate` (Linux/macOS)
или `.venv\Scripts\Activate.ps1` (Windows PowerShell).

```bash
pip install -r requirements.txt
```

Скопируйте `.env.example` в `.env`.

```bash
fastapi dev app/main.py
```

Документация: http://127.0.0.1:8000/docs

## Ручная проверка
1. Создайте два заказа через POST /orders: 201 и разные id.
2. Измените quantity у одного: остальные поля и created_at сохраняются.
3. Переведите заказ в completed: 200.
4. Попробуйте изменить его имя, вернуть pending, отправить пустой PATCH
   или удалить: во всех случаях 409 с detail.
5. Обратитесь к отсутствующему id через GET, PATCH и DELETE: 404 с detail.
6. Удалите незавершённый заказ: 204 без тела. Создайте новый: id не повторяется.
7. Проверьте фильтр status, sort_by=drink, limit и offset.
8. Некорректные размер/статус, quantity=0, limit=0 и offset=-1: 422.
9. GET /info возвращает фактическое число сохранённых заказов.

## Проверка сервиса без HTTP

```python
from app.repository import OrderRepository
from app.service import OrderService
from app.schemas import OrderCreate, OrderUpdate
from app.exceptions import OrderAlreadyCompletedError

service = OrderService(OrderRepository())
order = service.create_order(OrderCreate(drink="Латте", size="medium", quantity=1))
service.update_order(order.id, OrderUpdate(status="completed"))
try:
    service.cancel_order(order.id)
except OrderAlreadyCompletedError as error:
    print(error)
else:
    raise AssertionError("Удаление выполненного заказа должно быть запрещено")
```
