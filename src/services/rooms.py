from datetime import date

from src.exceptions import validate_dates, check_date_to_after_date_from, ObjectNotFoundException, \
    RoomNotFoundException, RoomHasActiveBookingsException, EmptyAllFieldsException, EmptyTitleFieldException, \
    RoomAlreadyExistsException, EmptyPriceFieldException, NegativePriceException, EmptyQuantityFieldException, \
    NegativeQuantityException, FacilityNotFoundException
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAddRequest, Room, RoomAdd, RoomPatchRequest, RoomPatch
from src.services.base import BaseService
from src.services.hotels import HotelService


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

        # Проверка 1: Все ли поля пустые
        if (not room_data.title and
                not room_data.description and
                room_data.price is None and
                room_data.quantity is None):
            raise EmptyAllFieldsException

        # Проверка 2: Обязательное поле title
        if not room_data.title or not room_data.title.strip():
            raise EmptyTitleFieldException

        # Проверка 3: Уникальность title (регистронезависимо)
        room_data.title = room_data.title.strip()
        existing_rooms = await self.db.rooms.get_filtered()
        if any(room.title.lower() == room_data.title.lower() for room in existing_rooms):
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
            existing_facilities = await self.db.facilities.get_all()
            existing_facility_ids = {facility.id for facility in existing_facilities}

            for facility_id in room_data.facilities_ids:
                if facility_id not in existing_facility_ids:
                    raise FacilityNotFoundException

        # Создаем номер
        room_data.description = room_data.description.strip() if room_data.description else None
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        room: Room = await self.db.rooms.add(_room_data)

        # Создаем связи с удобствами
        if room_data.facilities_ids:
            rooms_facilities_data = [
                RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
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
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        await self.db.rooms.edit(_room_data, id=room_id)
        await self.db.rooms_facilities.set_room_facilities(room_id, facilities_ids=room_data.facilities_ids)
        await self.db.commit()

    async def partially_edit_room(
            self,
            hotel_id: int,
            room_id: int,
            room_data: RoomPatchRequest,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        await self.db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.set_room_facilities(
                room_id, facilities_ids = _room_data_dict["facilities_ids"]
            )
            await self.db.commit()

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
