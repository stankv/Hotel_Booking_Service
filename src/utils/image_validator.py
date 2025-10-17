import os
from fastapi import UploadFile
from PIL import Image
import imghdr

from src.exceptions import InvalidImageException, ImageTooLargeException


class ImageValidator:
    # Допустимые MIME-типы изображений
    ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/bmp"}

    # Допустимые расширения файлов
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}

    # Максимальный размер файла (10 МБ)
    MAX_FILE_SIZE = 10 * 1024 * 1024

    @staticmethod
    def validate_image_file(file: UploadFile) -> None:
        """
        Валидация загружаемого изображения
        """
        # Проверка размера файла
        if file.size and file.size > ImageValidator.MAX_FILE_SIZE:
            raise ImageTooLargeException

        # Проверка MIME-типа
        if file.content_type not in ImageValidator.ALLOWED_MIME_TYPES:
            raise InvalidImageException

        # Проверка расширения файла
        file_extension = os.path.splitext(file.filename.lower())[1]
        if file_extension not in ImageValidator.ALLOWED_EXTENSIONS:
            raise InvalidImageException

    @staticmethod
    def validate_image_content(file: UploadFile) -> None:
        """
        Более строгая проверка содержимого изображения (синхронная версия)
        """
        # Сохраняем текущую позицию файла
        current_position = file.file.tell()

        # Читаем первые несколько байт для определения типа файла
        header = file.file.read(32)
        file.file.seek(current_position)  # Возвращаем указатель на исходную позицию

        # Проверяем сигнатуры файлов изображений
        image_type = imghdr.what(None, header)
        if not image_type:
            raise InvalidImageException

        # Дополнительная проверка с помощью PIL
        try:
            # Сохраняем позицию снова
            current_position = file.file.tell()
            image = Image.open(file.file)
            image.verify()  # Проверяем целостность изображения
            file.file.seek(current_position)  # Возвращаем указатель
        except Exception:
            raise InvalidImageException
