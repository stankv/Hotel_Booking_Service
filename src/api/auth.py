from fastapi import APIRouter, HTTPException, Response

from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/login",
             summary="Аутентификация",
             description="<h1>Аутентификация (вход) пользователя</h1>"
             )
async def login_user(
        data: UserRequestAdd,
        response: Response,
        db: DBDep,
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/register",
             summary="Регистрация",
             description="<h1>Регистрация нового пользователя</h1>"
             )
async def register_user(
        data: UserRequestAdd,
        db: DBDep,
):
    try:
        hashed_password = AuthService().hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        await db.users.add(new_user_data)
        await db.commit()
    except:    # noqa: E722
        raise HTTPException(status_code=400)
    return {"status": "OK"}


@router.get("/me",
            summary="Получение данных текущего пользователя",
            description="<h1>Получение данных текущего пользователя из JWT-токена</h1>"
            )
async def get_me(user_id: UserIdDep, db: DBDep):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
