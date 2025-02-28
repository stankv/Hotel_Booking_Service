from datetime import date

from fastapi import APIRouter, Body, Query
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch
from src.api.dependencies import DBDep

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms",
            summary="Получение ВСЕХ номеров конкретного отеля",
            description="<h1>Все номера по конкретному id отеля</h1>"
            )
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2024-08-01", description="Дата заезда"),
        date_to: date = Query(example="2024-08-10", description="Дата выезда"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}",
            summary="Получение номера по его ID",
            description="<h1>Получение номера по его ID</h1>"
            )
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms",
             summary="Добавление нового номера",
             description="<h1>Добавление нового номера</h1>"
             )
async def create_room(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}",
            summary="Изменение ВСЕХ данных номера",
            description="<h1>Ввод данных для всех полей обязателен</h1>"
            )
async def update_room(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}",
           summary="Частичное изменение данных номера",
           description="<h1>Можно изменить любое поле</h1>"
           )
async def partially_update_room(hotel_id: int, room_id: int, room_data: RoomPatchRequest, db: DBDep):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}",
               summary="Удаление номера",
               description="<h1>Удаление номера по его id у конкретного отеля</h1>")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
