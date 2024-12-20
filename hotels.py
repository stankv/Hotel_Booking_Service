from fastapi import Query, APIRouter, Body
from schemas.hotels import Hotel, HotelPATCH
from dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get("",
            summary="Получение ВСЕХ отелей / конкретного отеля",
            description="<h1>Все отели: поля ввода ID и title пусты<br>"
                        "Конкретный отель: поиск по любому полю</h1>"
            )
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="ID отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    if pagination.page and pagination.per_page:
        start = (pagination.page - 1) * pagination.per_page
        end = start + pagination.per_page
        hotels_ = hotels_[start:end]
    return hotels_


@router.post("",
             summary="Добавление нового отеля",
             description="<h1>Ввод title И name обязателен</h1>"
             )
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "name": "sochi_u_morya",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай У фонтана",
            "name": "dubai_fountain",
        }
    }
})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
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