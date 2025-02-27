from fastapi import APIRouter

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIdDep, PaginationDep

router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])

@router.get("",
            summary="Получение ВСЕХ бронирований",
            description="<h1>Все бронирования</h1><br>"
            )
async def get_bookings(
        pagination: PaginationDep,
        db: DBDep,
):
    per_page = pagination.per_page or 5
    return await db.bookings.get_all(offset=(pagination.page - 1) * per_page)


@router.post("",
             summary="<Бронирование номера",
             description="<h1>Добавление бронирования</h1><br>"
             )
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest,
):
    if user_id is None:
        return {"status": "ERROR", "message": "Пользователь не авторизован"}
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data":booking}
