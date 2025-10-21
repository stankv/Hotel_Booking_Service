from pydantic import BaseModel, ConfigDict
from src.schemas.facilities import FacilityDTO


class RoomAddRequestDTO(BaseModel):
    title: str
    description: str | None = None  # при вариативности надо задавать значение
    price: int
    quantity: int
    facilities_ids: list[int] = []


class RoomAddDTO(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int


class RoomDTO(RoomAddDTO):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RoomWithRelationshipsDTO(RoomDTO):
    facilities: list[FacilityDTO]


class RoomPatchRequestDTO(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []


class RoomPatchDTO(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
