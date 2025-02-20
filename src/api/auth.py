from fastapi import APIRouter, HTTPException, Response, Request

from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/login",
             summary="Аутентификация",
             description="<h1>Аутентификация (вход) пользователя</h1>"
             )
async def login_user(
        data: UserRequestAdd,
        response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.post("/register",
             summary="Регистрация",
             description="<h1>Регистрация нового пользователя</h1>"
             )
async def register_user(
        data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
        return {"status": "OK"}


@router.get("/only_auth",
            summary="Получение данных пользователя",
            description="<h1>Получение данных пользователя из JWT-токена</h1>"
            )
async def only_auth(request: Request) -> dict | None:
    access_token = request.cookies.get("access_token", None)
    data = AuthService().decode_token(access_token)
    user_id = data["user_id"]
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user