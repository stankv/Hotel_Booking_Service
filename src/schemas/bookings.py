from datetime import date

from pydantic import BaseModel, ConfigDict


class AddBookings(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class Bookings(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    model_config = ConfigDict(from_attributes=True)
