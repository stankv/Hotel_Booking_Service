from datetime import date
from fastapi import HTTPException


class HotelBookingServiceException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(HotelBookingServiceException):
    detail = "Объект не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class ObjectAlreadyExistsException(HotelBookingServiceException):
    detail = "Похожий объект уже существует"


class AllRoomsAreBookedException(HotelBookingServiceException):
    detail = "Не осталось свободных номеров"


class IncorrectTokenException(HotelBookingServiceException):
    detail = "Некорректный токен"


class EmailNotRegisteredException(HotelBookingServiceException):
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordException(HotelBookingServiceException):
    detail = "Пароль неверный"


class UserAlreadyExistsException(HotelBookingServiceException):
    detail = "Пользователь уже существует"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")


class HotelBookingServiceHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(HotelBookingServiceHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(HotelBookingServiceHTTPException):
    status_code = 404
    detail = "Номер не найден"


class AllRoomsAreBookedHTTPException(HotelBookingServiceHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class IncorrectTokenHTTPException(HotelBookingServiceHTTPException):
    detail = "Некорректный токен"


class EmailNotRegisteredHTTPException(HotelBookingServiceHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"


class UserEmailAlreadyExistsHTTPException(HotelBookingServiceHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"


class IncorrectPasswordHTTPException(HotelBookingServiceHTTPException):
    status_code = 401
    detail = "Пароль неверный"


class NoAccessTokenHTTPException(HotelBookingServiceHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"
