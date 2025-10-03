import shutil  # библиотека для сохранения файлов
from fastapi import APIRouter, UploadFile, BackgroundTasks

from src.exceptions import InvalidImageException, InvalidImageHTTPException, ImageTooLargeException, \
    ImageTooLargeHTTPException
from src.services.images import ImagesService
from src.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения отелей"])


@router.post(
    "",
    summary="Добавление изображения",
    description="<h1>Добавление фото отеля</h1>"
                "<p><b>Поддерживаемые форматы:</b> JPG, PNG, GIF, WEBP, BMP</p>"
                "<p><b>Максимальный размер:</b> 10 МБ</p>",
)
def upload_image(file: UploadFile, background_tasks: BackgroundTasks):
    try:
        ImagesService().upload_image(file, background_tasks)
    except InvalidImageException:
        raise InvalidImageHTTPException
    except ImageTooLargeException:
        raise ImageTooLargeHTTPException

    return {"status": "OK", "message": "Изображение успешно загружено", "filename": file.filename}
