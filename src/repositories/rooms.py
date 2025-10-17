from datetime import date

from sqlalchemy import select, func
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.exceptions import RoomNotFoundException
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelationshipsMapper
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDataMapper

    async def get_filtered_by_time(self, hotel_id, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(self.model)  # type: ignore
            .options(selectinload(self.model.facilities))  # type: ignore
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))  # type: ignore
        )
        result = await self.session.execute(query)
        return [
            RoomDataWithRelationshipsMapper.map_to_domain_entity(r)
            for r in result.unique().scalars().all()
        ]

    async def get_one_with_relationships(self, **filter_by):
        query = (
            select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by)  # type: ignore
        )
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise RoomNotFoundException
        return RoomDataWithRelationshipsMapper.map_to_domain_entity(model)

    async def has_active_bookings(self, room_id: int) -> bool:
        from src.models.bookings import BookingsOrm
        from sqlalchemy import select

        # Проверяем есть ли активные бронирования для этого номера
        query = select(BookingsOrm).where(
            BookingsOrm.room_id == room_id,
            BookingsOrm.date_to >= func.current_date(),  # Бронирования, которые еще активны
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None
