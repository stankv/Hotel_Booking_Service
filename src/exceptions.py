class HotelBookingServiceException(Exception):    # создаем свое базовое исключение
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):          # наследуемся от класса Exception
        super().__init__(self.detail, *args, **kwargs) # со всеми его параметрами и методами


class ObjectNotFoundException(HotelBookingServiceException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(HotelBookingServiceException):
    detail = "Не осталось свободных номеров"