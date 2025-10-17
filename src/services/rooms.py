from datetime import date

from src.exceptions import (
    ObjectNotFoundException,
    RoomNotFoundException,
    RoomHasActiveBookingsException,
)
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAddRequest, Room, RoomAdd, RoomPatchRequest, RoomPatch
from src.services.base import BaseService
from src.services.hotels import HotelService
from src.utils.date_validator import validate_dates, check_date_to_after_date_from
from src.utils.room_validator import RoomValidator


class RoomService(BaseService):
    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        # Валидируем даты через сервисные исключения
        validate_dates(date_from, date_to)
        check_date_to_after_date_from(date_from, date_to)

        await HotelService(self.db).get_hotel_with_check(hotel_id)
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(self, room_id: int, hotel_id: int):
        await self.get_room_with_check(room_id)
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        return await self.db.rooms.get_one_with_relationships(id=room_id, hotel_id=hotel_id)

    async def create_room(
        self,
        hotel_id: int,
        room_data: RoomAddRequest,
    ):
        # Проверяем существование отеля
        await HotelService(self.db).get_hotel_with_check(hotel_id)

        # Валидируем данные номера
        await RoomValidator.validate_room_data(self.db, room_data)

        # Очищаем description от пробелов
        RoomValidator.clean_room_description(room_data)

        # Создаем номер
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room: Room = await self.db.rooms.add(_room_data)

        # Создаем связи с удобствами
        if room_data.facilities_ids:
            rooms_facilities_data = [
                RoomFacilityAdd(room_id=room.id, facility_id=f_id)
                for f_id in room_data.facilities_ids
            ]
            await self.db.rooms_facilities.add_bulk(rooms_facilities_data)

        await self.db.commit()
        return room

    async def edit_room(
        self,
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        # Валидируем данные номера (передаем room_id для исключения текущего номера из проверки уникальности)
        await RoomValidator.validate_room_data(self.db, room_data, exclude_room_id=room_id)

        # Очищаем description от пробелов
        RoomValidator.clean_room_description(room_data)

        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(_room_data, id=room_id)
        await self.db.rooms_facilities.set_room_facilities(
            room_id, facilities_ids=room_data.facilities_ids
        )
        await self.db.commit()
        # Возвращаем обновленный номер с отношениями (удобствами)
        return await self.db.rooms.get_one_with_relationships(id=room_id, hotel_id=hotel_id)

    async def partially_edit_room(
        self,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        current_room = await self.get_room_with_check(room_id)

        # Валидируем только переданные данные
        await RoomValidator.validate_partial_room_data(
            self.db, room_data, current_room, exclude_room_id=room_id
        )

        # Очищаем description если он был передан
        if room_data.description is not None:
            room_data.description = room_data.description.strip()

        # Подготавливаем данные для обновления
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)

        # Обновляем номер
        await self.db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)

        # Обновляем связи с удобствами если передан facilities_ids
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id, facilities_ids=_room_data_dict["facilities_ids"]
            )

        await self.db.commit()

        # Возвращаем обновленный номер с отношениями
        return await self.db.rooms.get_one_with_relationships(id=room_id, hotel_id=hotel_id)

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)
        # Проверяем есть ли активные бронирования
        if await self.db.rooms.has_active_bookings(room_id):
            raise RoomHasActiveBookingsException
        # Сначала удаляем все связи номера с удобствами
        await self.db.rooms_facilities.delete(room_id=room_id)
        # Затем удаляем сам номер
        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
