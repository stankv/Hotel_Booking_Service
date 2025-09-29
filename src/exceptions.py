from datetime import date
from fastapi import HTTPException

from src.config import settings


class HotelBookingServiceException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class EmptyAllFieldsException(HotelBookingServiceException):
    detail = "Не переданы все поля"


class EmptyFieldException(HotelBookingServiceException):
    detail = "Пустое поле"


class EmptyTitleFieldException(EmptyFieldException):
        detail = "Не передано название"


class EmptyLocationFieldException(EmptyFieldException):
    detail = "Не передан адрес"


class ObjectNotFoundException(HotelBookingServiceException):
    detail = "Объект не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class ObjectAlreadyExistsException(HotelBookingServiceException):
    detail = "Такой объект уже существует"


class AllRoomsAreBookedException(HotelBookingServiceException):
    detail = "Не осталось свободных номеров"


class RoomHasActiveBookingsException(HotelBookingServiceException):
    detail = "Номер имеет активное бронирование!"


class IncorrectTokenException(HotelBookingServiceException):
    detail = "Некорректный токен"


class EmailNotRegisteredException(HotelBookingServiceException):
    detail = "Пользователь с таким email не зарегистрирован"


class IncorrectPasswordException(HotelBookingServiceException):
    detail = "Пароль неверный"


class IncorrectPasswordRegisterException(HotelBookingServiceException):
    detail = "Некорректный пароль при регистрации"


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


class ObjectAlreadyExistsHTTPException(HotelBookingServiceHTTPException):
    status_code = 409
    detail = "Объект уже существует"

class HotelNotFoundHTTPException(HotelBookingServiceHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(HotelBookingServiceHTTPException):
    status_code = 404
    detail = "Номер не найден"


class RoomHasActiveBookingsHTTPException(HotelBookingServiceHTTPException):
    status_code = 409
    detail = "Нельзя удалить номер с активным бронированием!"


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


class IncorrectPasswordRegisterHTTPException(HotelBookingServiceHTTPException):
    status_code = 406
    detail = f"Пароль должен быть не менее {settings.MIN_LENGTH_PASSWORD} символов!"


class NoAccessTokenHTTPException(HotelBookingServiceHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"


class EmptyAllFieldsHTTPException(HotelBookingServiceHTTPException):
    status_code = 400
    detail = "Не передано ни одно значение"


class EmptyTitleFieldHTTPException(HotelBookingServiceHTTPException):
    status_code = 400
    detail = "Не передано название. Пустое поле title"


class EmptyLocationFieldHTTPException(HotelBookingServiceHTTPException):
    status_code = 400
    detail = "Не передан адрес. Пустое поле location"
