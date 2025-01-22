from fastapi import Query, APIRouter, Body
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep

from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from sqlalchemy import insert, select, func

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("",
            summary="Получение ВСЕХ отелей / конкретного отеля",
            description="<h1>Все отели: поля ввода title и location пусты<br>"
                        "Конкретный отель: поиск по любому полю</h1>"
            )
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description=" Адрес отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if title:
            query = query.filter(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(HotelsOrm.location).contains(location.strip().lower()))
        query = (
            query
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels
    # if pagination.page and pagination.per_page:
    #     start = (pagination.page - 1) * pagination.per_page
    #     end = start + pagination.per_page
    #     hotels_ = hotels_[start:end]
    # return hotels_


@router.post("",
             summary="Добавление нового отеля",
             description="<h1>Ввод title И location обязателен</h1>"
             )
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "location": "ул. Моря, 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай У фонтана",
            "location": "ул. Шейха, 2",
        }
    }
})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}",
            summary="Изменение ВСЕХ данных отеля",
            description="<h1>Ввод title И name обязателен</h1>"
            )
def update_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            break
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частичное изменение данных отеля",
           description="<h1>Можно изменить title, а можно name</h1>"
           )
def partially_update_hotel(id: int, hotel_data: HotelPATCH):
    global hotels
    if hotel_data.title is None and hotel_data.name is None:
        return {"status": "Data not changed"}
    for hotel in hotels:
        if hotel["id"] == id:
            if hotel_data.title is not None and hotel_data.title != "string":
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None and hotel_data.name != "string":
                hotel["name"] = hotel_data.name
            break
    return {"status": "OK"}


@router.delete("/{hotel_id}",
               summary="Удаление отеля",
               description="<h1>Удаление отеля</h1>")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}