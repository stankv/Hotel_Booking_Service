import shutil

from fastapi import UploadFile, BackgroundTasks

from src.services.base import BaseService
from src.tasks.tasks import resize_image
from src.utils.image_validator import ImageValidator


class ImagesService(BaseService):
    def upload_image(self, file: UploadFile, background_tasks: BackgroundTasks):
        # Валидация изображения
        ImageValidator.validate_image_file(file)

        # Дополнительная проверка содержимого (синхронно)
        ImageValidator.validate_image_content(file)

        # Создаем путь для сохранения
        image_path = f"src/static/images/{file.filename}"
        # Сохраняем файл
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        # Добавляем задачу по изменению размера
        # resize_image.delay(image_path)
        background_tasks.add_task(resize_image, image_path)
