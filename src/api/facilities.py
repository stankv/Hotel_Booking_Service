from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import (
    ObjectAlreadyExistsException,
    ObjectAlreadyExistsHTTPException,
    EmptyTitleFieldHTTPException,
    EmptyTitleFieldException,
)
from src.schemas.facilities import FacilityAddDTO
from src.services.facilities import FacilityService

router = APIRouter(prefix="/facilities", tags=["Удобства номеров"])


@router.get("", summary="Получение ВСЕХ удобств", description="<h1>Все удобства номеров</h1>")
@cache(expire=10)
async def get_facilities(db: DBDep):
    return await FacilityService(db).get_facilities()


@router.post(
    "",
    summary="Добавление нового удобства",
    description="<h1>Добавление нового удобства в список всех удобств</h1>",
)
async def create_facility(db: DBDep, facility_data: FacilityAddDTO = Body()):
    try:
        facility = await FacilityService(db).create_facility(facility_data)
    except EmptyTitleFieldException:
        raise EmptyTitleFieldHTTPException
    except ObjectAlreadyExistsException:
        raise ObjectAlreadyExistsHTTPException
    return {"status": "OK", "data": facility}
