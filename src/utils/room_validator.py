from src.exceptions import (
    EmptyAllFieldsException,
    EmptyTitleFieldException,
    EmptyPriceFieldException,
    EmptyQuantityFieldException,
    NegativePriceException,
    NegativeQuantityException,
    RoomAlreadyExistsException,
    FacilityNotFoundException,
)
from src.schemas.rooms import RoomAddRequestDTO, RoomPatchRequestDTO


class RoomValidator:
    @staticmethod
    async def validate_room_data(
        db, room_data: RoomAddRequestDTO, exclude_room_id: int | None = None
    ) -> None:
        """
        Валидация данных номера (используется при создании и обновлении)

        Args:
            db: Экземпляр DBManager
            room_data: Данные номера для валидации
            exclude_room_id: ID номера для исключения при проверке уникальности
        """
        # Проверка 1: Все ли поля пустые
        if (
            not room_data.title
            and not room_data.description
            and room_data.price is None
            and room_data.quantity is None
        ):
            raise EmptyAllFieldsException

        # Проверка 2: Обязательное поле title
        if not room_data.title or not room_data.title.strip():
            raise EmptyTitleFieldException

        # Очищаем title от пробелов
        room_data.title = room_data.title.strip()

        # Проверка 3: Уникальность title (регистронезависимо), исключая текущий номер
        existing_rooms = await db.rooms.get_filtered()
        if any(
            room.title.lower() == room_data.title.lower() and room.id != exclude_room_id
            for room in existing_rooms
        ):
            raise RoomAlreadyExistsException

        # Проверка 4: Обязательное поле price и его валидность
        if room_data.price is None:
            raise EmptyPriceFieldException
        if room_data.price < 0:
            raise NegativePriceException

        # Проверка 5: Обязательное поле quantity и его валидность
        if room_data.quantity is None:
            raise EmptyQuantityFieldException
        if room_data.quantity < 0:
            raise NegativeQuantityException

        # Проверка 6: Валидация facilities_ids
        if room_data.facilities_ids:
            existing_facilities = await db.facilities.get_all()
            existing_facility_ids = {facility.id for facility in existing_facilities}

            for facility_id in room_data.facilities_ids:
                if facility_id not in existing_facility_ids:
                    raise FacilityNotFoundException

    @staticmethod
    def clean_room_description(room_data: RoomAddRequestDTO) -> None:
        """
        Очистка поля description от пробелов
        """
        if room_data.description is not None:
            room_data.description = room_data.description.strip()

    @staticmethod
    async def validate_partial_room_data(
        db, room_data: RoomPatchRequestDTO, current_room_data, exclude_room_id: int | None = None
    ) -> None:
        """
        Валидация данных номера для частичного обновления
        Проверяет только переданные параметры
        """
        # Проверка 1: Передан ли хотя бы один параметр с не-None значением
        data_dict = room_data.model_dump(exclude_unset=True)

        # Удаляем facilities_ids из проверки на пустоту, так как это отдельный случай
        check_dict = {k: v for k, v in data_dict.items() if k != "facilities_ids"}

        if not check_dict and not data_dict.get("facilities_ids"):
            raise EmptyAllFieldsException

        # Проверка 2: Если передан title - проверяем его
        if room_data.title is not None:
            if not room_data.title.strip():
                raise EmptyTitleFieldException

            # Очищаем title от пробелов
            room_data.title = room_data.title.strip()

            # Проверяем уникальность (исключая текущий номер)
            existing_rooms = await db.rooms.get_filtered()
            if any(
                room.title.lower() == room_data.title.lower() and room.id != exclude_room_id
                for room in existing_rooms
            ):
                raise RoomAlreadyExistsException

        # Проверка 3: Если передан price - проверяем его
        if room_data.price is not None:
            # Проверяем что значение не None (дополнительная проверка)
            if room_data.price is None:
                raise EmptyPriceFieldException
            # Проверяем что значение не отрицательное
            if room_data.price < 0:
                raise NegativePriceException

        # Проверка 4: Если передан quantity - проверяем его
        if room_data.quantity is not None:
            # Проверяем что значение не None (дополнительная проверка)
            if room_data.quantity is None:
                raise EmptyQuantityFieldException
            # Проверяем что значение не отрицательное
            if room_data.quantity < 0:
                raise NegativeQuantityException

        # Проверка 5: Если передан facilities_ids - проверяем их
        if room_data.facilities_ids is not None and room_data.facilities_ids:
            existing_facilities = await db.facilities.get_all()
            existing_facility_ids = {facility.id for facility in existing_facilities}

            for facility_id in room_data.facilities_ids:
                if facility_id not in existing_facility_ids:
                    raise FacilityNotFoundException
