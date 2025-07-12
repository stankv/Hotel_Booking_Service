from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="", tags=["Главная страница"])

@router.get(
    "/",
    summary="Главная страница",
    description="<h1>Ссылки на документацию (Swagger UI и ReDoc)</h1>",
)
async def root():
    data = """<h1>Сервис бронирования отелей</h1><br>
              <h2>BACKEND</h2>
              <p>
                <a href="./docs">Документация Swagger UI</a><br>
                <a href="./redoc">Документация ReDoc</a>
              </p>"""
    return HTMLResponse(content=data)