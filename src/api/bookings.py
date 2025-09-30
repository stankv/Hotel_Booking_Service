from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import AllRoomsAreBookedException, AllRoomsAreBookedHTTPException, InvalidDateException, \
    InvalidDateHTTPException, DateFromAfterDateToException, DateFromAfterDateToHTTPException
from src.schemas.bookings import BookingAddRequest
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get(
    "",
    summary="Получение ВСЕХ бронирований",
    description="<h1>Все бронирования</h1><br>",
)
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get(
    "/me",
    summary="Получение бронирований пользователя",
    description="<h1>Все бронирования пользователя</h1><h2>(нужно авторизоваться)</h2>",
)
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post(
    "",
    summary="Бронирование номера",
    description="<h1>Добавление бронирования</h1>",
)
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest,
):
    try:
        booking = await BookingService(db).add_booking(user_id, booking_data)
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException
    except InvalidDateException:
        raise InvalidDateHTTPException
    except DateFromAfterDateToException:
        raise DateFromAfterDateToHTTPException
    return {"status": "OK", "data": booking}
