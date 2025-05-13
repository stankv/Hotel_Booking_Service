from fastapi import APIRouter

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIdDep, PaginationDep

router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])

@router.get("",
            summary="Получение ВСЕХ бронирований",
            description="<h1>Все бронирования</h1><br>"
            )
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me",
            summary="Получение бронирований пользователя",
            description="<h1>Все бронирования пользователя</h1>"
                        "<h2>(нужно авторизоваться)</h2>"
            )
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("",
             summary="Бронирование номера",
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
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    await db.commit()
    return {"status": "OK", "data":booking}
