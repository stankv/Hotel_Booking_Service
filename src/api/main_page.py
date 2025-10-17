from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="", tags=["Главная страница"])


@router.get(
    "/",
    summary="Главная страница",
    description="<h1>Ссылки на документацию (Swagger UI и ReDoc)</h1>",
)
@router.head("/", include_in_schema=False)
async def root():
    data = """<!DOCTYPE html>
              <html lang="ru">
              <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Сервис бронирования отелей</title>
                <meta name="description" content="Бронирование номеров отелей">
              </head>
              <body>
                <h1>Сервис бронирования отелей</h1><br>
                <h2>BACKEND</h2>
                <p>
                  <a href="./docs">Документация Swagger UI</a><br>
                  <a href="./redoc">Документация ReDoc</a>
                </p>
                </body>
                </html>"""
    return HTMLResponse(content=data)
