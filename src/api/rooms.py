from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.exceptions import HotelNotFoundHTTPException, \
    RoomNotFoundHTTPException, RoomNotFoundException, HotelNotFoundException
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.api.dependencies import DBDep
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get(
    "/{hotel_id}/rooms",
    summary="Получение ВСЕХ номеров конкретного отеля",
    description="<h1>Все номера по конкретному id отеля</h1>",
)
@cache(expire=10)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01", description="Дата заезда"),
    date_to: date = Query(example="2024-08-10", description="Дата выезда"),
):
    return await RoomService(db).get_filtered_by_time(hotel_id, date_from, date_to)


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Получение номера по его ID",
    description="<h1>Получение номера по его ID</h1>",
)
@cache(expire=10)
async def get_room(room_id: int, hotel_id: int, db: DBDep):
    try:
        return await RoomService(db).get_room(room_id, hotel_id=hotel_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.post(
    "/{hotel_id}/rooms",
    summary="Добавление нового номера",
    description="<h1>Добавление нового номера</h1>",
)
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    try:
        room = await RoomService(db).create_room(hotel_id, room_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK", "data": room}


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Изменение ВСЕХ данных номера",
    description="<h1>Ввод данных для всех полей обязателен</h1>",
)
async def update_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    await RoomService(db).edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное изменение данных номера",
    description="<h1>Можно изменить любое поле</h1>",
)
async def partially_update_room(
    hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep
):
    await RoomService(db).partially_edit_room(hotel_id, room_id, room_data)
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление номера",
    description="<h1>Удаление номера по его id у конкретного отеля</h1>",
)
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await RoomService(db).delete_room(hotel_id, room_id)
    return {"status": "OK"}
