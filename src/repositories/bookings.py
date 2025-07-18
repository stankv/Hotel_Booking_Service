from datetime import date
from typing import Sequence
from fastapi import HTTPException

from sqlalchemy import select

from src.exceptions import AllRoomsAreBookedException
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checking(self):
        query = select(BookingsOrm).filter(BookingsOrm.date_from == date.today())
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: Sequence[int] = rooms_ids_to_book_res.scalars().all()

        if (
            data.room_id in rooms_ids_to_book
        ):  # если текущий номер в тех что можно бронировать, то бронируем
            new_booking = await self.add(data)
            return new_booking

        raise AllRoomsAreBookedException
