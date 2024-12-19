from fastapi import Query, Body, APIRouter

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
]

@router.get("",
            summary="Получение ВСЕХ отелей / конкретного отеля",
            description="<h1>Все отели: поля ввода ID и title пусты<br>"
                        "Конкретный отель: поиск по любому полю</h1>"
            )
def get_hotels(
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
    return hotels_


@router.post("",
             summary="Добавление нового отеля",
             description="<h1>Ввод title И name обязателен</h1>"
             )
def create_hotel(
        title: str = Body(embed=True, description="Название отеля"),
        name: str = Body(embed=True, description="транскрипция названия отеля"),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
    return {"status": "OK"}


@router.put("/{hotel_id}",
            summary="Изменение ВСЕХ данных отеля",
            description="<h1>Ввод title И name обязателен</h1>"
            )
def update_hotel(
        hotel_id: int,
        title: str = Body(embed=True),
        name: str = Body(embed=True),
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            break
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частичное изменение данных отеля",
           description="<h1>Можно изменить title, а можно name</h1>"
           )
def partially_update_hotel(
        id: int,
        title: str | None = Body(None, embed=True, description="Название отеля"),
        name: str | None = Body(None, embed=True, description="транскрипция названия отеля"),
):
    global hotels
    if title is None and name is None:
        return {"status": "Data not changed"}
    for hotel in hotels:
        if hotel["id"] == id:
            if title is not None and title != "string":
                hotel["title"] = title
            if name is not None and name != "string":
                hotel["name"] = name
            break
    return {"status": "OK"}


@router.delete("/{hotel_id}",
               summary="Удаление отеля",
               description="<h1>Удаление отеля</h1>")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}