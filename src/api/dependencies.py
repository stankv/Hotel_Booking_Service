from typing import Annotated
from fastapi import Depends, Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, gt=0, description="Номер страницы")]
    per_page: Annotated[int | None, Query(None, gt=0, lt=30, description="Количество элементов на странице")]


PaginationDep = Annotated[PaginationParams, Depends()]
