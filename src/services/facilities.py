from src.exceptions import ObjectAlreadyExistsException, EmptyTitleFieldException
from src.schemas.facilities import FacilityAddDTO
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilityService(BaseService):
    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def create_facility(self, data: FacilityAddDTO):
        if not data.title.strip():
            raise EmptyTitleFieldException

        data.title = data.title.strip()
        facilities = await self.get_facilities()
        if any(item.title.lower() == data.title.lower() for item in facilities):
            raise ObjectAlreadyExistsException

        facility = await self.db.facilities.add(data)
        await self.db.commit()

        test_task.delay()  # type: ignore

        return facility
