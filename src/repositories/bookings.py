from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.schemas.bookings import Bookings


class RoomsRepository(BaseRepository):
    model = BookingsOrm
    schema = Bookings