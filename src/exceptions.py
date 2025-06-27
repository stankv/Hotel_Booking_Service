from datetime import date

from fastapi import HTTPException


class HotelBookingServiceException(Exception):    # создаем свое базовое исключение
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):          # наследуемся от класса Exception
        super().__init__(self.detail, *args, **kwargs) # со всеми его параметрами и методами


class ObjectNotFoundException(HotelBookingServiceException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(HotelBookingServiceException):
    detail = "Похожий объект уже существует"


class AllRoomsAreBookedException(HotelBookingServiceException):
    detail = "Не осталось свободных номеров"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда!")


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