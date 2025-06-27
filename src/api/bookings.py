from fastapi import APIRouter, HTTPException

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import DBDep, UserIdDep  # PaginationDep?
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, RoomNotFoundHTTPException
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room

router = APIRouter(prefix="/bookings", tags=["Бронирование номеров"])


@router.get(
    "",
    summary="Получение ВСЕХ бронирований",
    description="<h1>Все бронирования</h1><br>",
)
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get(
    "/me",
    summary="Получение бронирований пользователя",
    description="<h1>Все бронирования пользователя</h1><h2>(нужно авторизоваться)</h2>",
)
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post(
    "",
    summary="Бронирование номера",
    description="<h1>Добавление бронирования</h1><br>",
)
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest,
):
    if user_id is None:
        return {"status": "ERROR", "message": "Пользователь не авторизован"}
    try:
        room: Room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise RoomNotFoundHTTPException
    hotel: Hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump(),
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": booking}
