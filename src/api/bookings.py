from fastapi import Query, APIRouter, Body

from src.schemas.bookings import Bookings, AddBookings
from src.api.dependencies import PaginationDep, DBDep


router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])

@router.post("/bookings")
async def create_booking(db: DBDep, bookings_data: AddBookings = Body()):
    user_id: int = 1  # получить значение из куки (из токена)
    price = 1000      # получить значение из конкретного номера конкретного отеля
    if user_id is None:
        return {"status": "ERROR", "message": "Пользователь не авторизован"}
    _bookings_data = Bookings(id=user_id, price=price,**bookings_data.model_dump())
    bookings = await db.bookings.add(_bookings_data)
    await db.commit()
    return {"status": "OK", "data":bookings}