from datetime import date

from src.exceptions import DateFromAfterDateToException, InvalidDateException


def validate_date_format(date_str: str) -> date:
    """
    Валидирует строку даты в формате YYYY-MM-DD
    Проверяет корректность формата и допустимость значений
    """
    try:
        # Проверяем базовый формат
        if len(date_str) != 10 or date_str[4] != "-" or date_str[7] != "-":
            raise ValueError("Invalid date format")

        year, month, day = map(int, date_str.split("-"))

        # Проверяем допустимые диапазоны
        if year < 1900 or year > 2100:
            raise ValueError("Invalid year")
        if month < 1 or month > 12:
            raise ValueError("Invalid month")
        if day < 1 or day > 31:
            raise ValueError("Invalid day")

        # Проверяем конкретную дату (например, 31 февраля)
        validated_date = date(year, month, day)

        # Проверяем что дата не в прошлом (для бронирований)
        if validated_date < date.today():
            raise ValueError("Date in past")

        return validated_date

    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid date: {str(e)}")


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise DateFromAfterDateToException


def validate_dates(date_from: date, date_to: date) -> None:
    """
    Валидирует даты и выбрасывает соответствующие сервисные исключения
    """
    try:
        # Преобразуем в строку и обратно для единообразной обработки
        date_from_str = date_from.isoformat() if isinstance(date_from, date) else str(date_from)
        date_to_str = date_to.isoformat() if isinstance(date_to, date) else str(date_to)

        validate_date_format(date_from_str)
        validate_date_format(date_to_str)

    except ValueError:
        raise InvalidDateException
