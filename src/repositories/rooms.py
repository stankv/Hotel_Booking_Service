from datetime import date
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room, RoomWithRelationships
from src.repositories.utils import rooms_ids_for_booking
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRelationships.model_validate(r) for r in result.unique().scalars().all()]


    async  def get_room_with_facilities(self, room_id: int, hotel_id: int):
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.hotel_id == hotel_id, RoomsOrm.id == room_id)
        )
        result = await self.session.execute(query)
        return RoomWithRelationships.model_validate(result.unique().scalars().one_or_none())
