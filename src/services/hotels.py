from datetime import date

from src.exceptions import validate_dates, check_date_to_after_date_from, ObjectNotFoundException, HotelNotFoundException, \
    EmptyTitleFieldException, EmptyLocationFieldException, ObjectAlreadyExistsException, EmptyAllFieldsException
from src.schemas.hotels import HotelAdd, HotelPatch, Hotel
from src.services.base import BaseService


class HotelService(BaseService):
    async def get_filtered_by_time(
            self,
            pagination,
            location: str | None,
            title: str | None,
            date_from: date,
            date_to: date,
    ):
        # Валидируем даты через сервисные исключения
        validate_dates(date_from, date_to)
        check_date_to_after_date_from(date_from, date_to)

        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex

    async def get_all_hotels(self):
        return await self.db.hotels.get_full_all()

    async def get_hotel(self, hotel_id: int):
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, data: HotelAdd):
        if (not data.title.strip()) and (not data.location.strip()):
            raise EmptyAllFieldsException
        if not data.title.strip():
            raise EmptyTitleFieldException
        if not data.location.strip():
            raise EmptyLocationFieldException
        data.title = data.title.strip()
        data.location = data.location.strip()
        all_hotels = await self.get_all_hotels()
        if any(item.title.lower() == data.title.lower() for item in all_hotels):
            raise ObjectAlreadyExistsException
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel

    async def edit_hotel(self, hotel_id: int, data: HotelAdd):
        await self.get_hotel_with_check(hotel_id=hotel_id)
        if (not data.title.strip()) and (not data.location.strip()):
            raise EmptyAllFieldsException
        if not data.title.strip():
            raise EmptyTitleFieldException
        if not data.location.strip():
            raise EmptyLocationFieldException
        data.title = data.title.strip()
        data.location = data.location.strip()
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()

    async def edit_hotel_partially(self, hotel_id: int, data: HotelPatch, exclude_unset: bool = False):
        await self.get_hotel_with_check(hotel_id=hotel_id)
        if (not data.title.strip()) and (not data.location.strip()):
            raise EmptyAllFieldsException
        if data.title:
            data.title = data.title.strip()
        if data.location:
            data.location = data.location.strip()
        await self.db.hotels.edit(data, exclude_unset=exclude_unset, id=hotel_id)
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.get_hotel_with_check(hotel_id=hotel_id)
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
