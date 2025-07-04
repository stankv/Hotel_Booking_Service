import shutil  # библиотека для сохранения файлов
from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.services.images import ImagesService
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post(
    "",
    summary="Добавление изображения",
    description="<h1>Добавление фото отеля</h1>",
)
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    ImagesService().upload_image(file, background_tasks)
