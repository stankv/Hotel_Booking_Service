from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

from src.init import redis_manager  # from src.init import redis_manager
from src.api.main_page import router as router_main_page
from src.api.auth import router as router_auth
from src.api.hotels import router as router_hotels
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images


@asynccontextmanager
async def lifespan(app: FastAPI):
    # При старте приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager._redis), prefix="fastapi-cache")
    logging.info("FastAPI cache initialized")
    yield
    # При выключении/перезагрузке приложения
    await redis_manager.close()


# Функция для добавления HEAD методов ко всем роутерам
# def add_head_methods_to_all_routes(app: FastAPI):
#     for route in app.routes:
#         if isinstance(route, APIRoute):
#             route.methods.add("HEAD")

app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://hotels-for-you.ru",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры (после добавления HEAD методов)
app.include_router(router_main_page)
app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_facilities)
app.include_router(router_bookings)
app.include_router(router_images)

# Добавляем HEAD методы ко всем роутерам
# add_head_methods_to_all_routes(app)

# --------------------------------------------------------------------------------------
# решение проблемы нкорректной работы документации
# https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/#disable-the-automatic-docs

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,    # type: ignore
        title=app.title + " - Swagger UI",    # type: ignore
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,    # type: ignore
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)    # type: ignore
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,    # type: ignore
        title=app.title + " - ReDoc",   # type: ignore
        redoc_js_url="https://unpkg.com/redoc@next/bundles/redoc.standalone.js",
    )
# --------------------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
