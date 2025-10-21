from fastapi import APIRouter, Response, Request

from src.api.dependencies import UserIdDep, DBDep
from src.config import settings
from src.exceptions import (
    IncorrectPasswordHTTPException,
    IncorrectPasswordException,
    EmailNotRegisteredHTTPException,
    EmailNotRegisteredException,
    UserAlreadyExistsException,
    UserEmailAlreadyExistsHTTPException,
    IncorrectPasswordRegisterException,
    IncorrectPasswordRegisterHTTPException,
)
from src.schemas.users import UserRequestAddDTO
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post(
    "/register",
    summary="Регистрация",
    description=f"<h1>Регистрация нового пользователя</h1>"
    f"<p><b>Пароль должен быть не меньше {settings.MIN_LENGTH_PASSWORD} символов!</b></p>",
)
async def register_user(
    data: UserRequestAddDTO,
    db: DBDep,
):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    except IncorrectPasswordRegisterException:
        raise IncorrectPasswordRegisterHTTPException
    return {"status": "OK"}


@router.post(
    "/login",
    summary="Аутентификация (Вход)",
    description="<h1>Аутентификация (вход) пользователя</h1>",
)
async def login_user(
    data: UserRequestAddDTO,
    response: Response,
    db: DBDep,
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get(
    "/me",
    summary="Получение данных текущего пользователя",
    description="<h1>Получение данных текущего пользователя из JWT-токена</h1>",
)
async def get_me(
    user_id: UserIdDep,
    db: DBDep,
):
    return await AuthService(db).get_one_or_none_user(user_id)


@router.post(
    "/logout",
    summary="Выход",
    description="<h1>Выход пользователя</h1>",
)
async def logout(response: Response, request: Request):
    access_token: str | None = request.cookies.get("access_token")
    if access_token:
        response.delete_cookie("access_token")
        return {"status": "OK", "detail": "Вы вышли из системы"}
    return {"status": "WARNING", "detail": "Вы уже вышли из системы или не были авторизованы"}
