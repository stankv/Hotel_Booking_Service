from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства номеров"])


@router.get("",
            summary="Получение ВСЕХ удобств",
            description="<h1>Все удобства номеров</h1>"
            )
@cache(expire=10)
async def get_facilities(db: DBDep):
        return await db.facilities.get_all()

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
