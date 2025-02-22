from pydantic import BaseModel, Field, ConfigDict


class RoomAddRequest(BaseModel):
    title: str
    description: str | None = None  # при вариативности надо задавать значение
    price: int
    quanity: int


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quanity: int


class Room(RoomAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class RoomPatchRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quanity: int | None = None


class RoomPatch(BaseModel):
    hotel_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quanity: int | None = None
