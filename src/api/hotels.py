from datetime import date

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.exceptions import ObjectNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelService


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение ВСЕХ отелей со свободными номерами",
    description="<h1>Все отели: поля ввода title и location пусты<br>"
    "Конкретный отель: поиск по любому полю</h1>",
)
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description=" Адрес отеля"),
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    return await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to,
    )


@router.get(
    "/all_or_one",
    summary="Получение ВСЕХ отелей / конкретного отеля",
    description="<h1>Все отели: поля ввода title и location пусты<br>"
    "Конкретный отель: поиск по любому полю</h1>",
)
@cache(expire=10)
async def get_all_hotels_or_one(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Название отеля"),
    location: str | None = Query(None, description=" Адрес отеля"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        title=title,
        location=location,
        limit=per_page,
        offset=(pagination.page - 1) * per_page,
    )


@router.get(
    "/{hotel_id}",
    summary="Получение отеля по его ID",
    description="<h1>Получение отеля по его ID</h1>",
)
@cache(expire=10)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        return await HotelService(db).get_hotel(hotel_id)
    except ObjectNotFoundException:
        raise HotelNotFoundHTTPException


@router.post(
    "",
    summary="Добавление нового отеля",
    description="<h1>Ввод title И location обязателен</h1>",
)
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель Сочи 5 звезд у моря",
                    "location": "ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель Дубай У фонтана",
                    "location": "ул. Шейха, 2",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).add_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Изменение ВСЕХ данных отеля",
    description="<h1>Ввод title И location обязателен</h1>",
)
async def update_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await HotelService(db).edit_hotel(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное изменение данных отеля",
    description="<h1>Можно изменить title, а можно location</h1>",
)
async def partially_update_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    if hotel_data.title is None and hotel_data.location is None:
        return {"status": "Data not changed"}
    await HotelService(db).edit_hotel_partially(hotel_id, hotel_data, exclude_unset=True)
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удаление отеля", description="<h1>Удаление отеля</h1>")
async def delete_hotel(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id)
    return {"status": "OK"}
