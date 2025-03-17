import json
from fastapi import APIRouter, Body
from src.api.dependencies import DBDep
from init import redis_manager    # from src.init import redis_manager
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства номеров"])


@router.get("",
            summary="Получение ВСЕХ удобств",
            description="<h1>Все удобства номеров</h1>"
            )
async def get_facilities(db: DBDep):
    facilities_from_cache = await redis_manager.get("facilities")    # получение данных по ключу facilities из кэша, если они есть
    if not facilities_from_cache:
        facilities = await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.model_dump() for f in facilities]    # создание словаря с данными для сериализации
        facilities_json = json.dumps(facilities_schemas)    # сериализация данных в формате json
        await redis_manager.set("facilities", facilities_json, 10)    # запись данных в кэш по ключу facilities
        return facilities
    else:
        facilities_dicts = json.loads(facilities_from_cache)    # десериализация данных из кэша
        return facilities_dicts


@router.post("",
             summary="Добавление нового удобства",
             description="<h1>Добавление нового удобства в список всех удобств</h1>"
             )
async def create_facility(
        db: DBDep,
        facility_data: FacilityAdd = Body()):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
