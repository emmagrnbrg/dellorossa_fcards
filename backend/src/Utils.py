import re
from datetime import datetime
from functools import wraps
from hashlib import sha512 as _sha512, sha1 as _sha1
from random import choice
from typing import Callable

from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Query

from backend.src.Constants import MAX_IMG_SIZE_BYTES, DIGITS
from backend.src.enums.TemplateEnum import TemplateEnum
from backend.src.enums.UsersEnum import RightEnum
from backend.src.models.PaginatedResponse import PaginatedResponse


def generateCode() -> str:
    """
    Генерация одноразового кода

    :return: одноразовый код
    """
    return "".join([choice(DIGITS) for _ in range(6)])


def isExpired(timestamp: datetime) -> bool:
    """
    Сравнение временной метки по сравнению с текущим временем

    :param timestamp: временная метка
    :return: признак того, что дата-время истекли
    """
    return not timestamp or timestamp <= datetime.now()


def readEmailTemplate(template: TemplateEnum) -> str:
    """
    Чтение шаблона электронного письма из репозитория

    :param template: наименование шаблона
    :return: данные шаблона
    """
    with open(str(template.value), "r", encoding="utf-8") as rf:
        return rf.read()


def sha512(openText: str) -> str:
    """
    Хеширование текста алгоритмом SHA512

    :param openText: открытый текст
    :return: закрытый текст
    """
    return _sha512(openText.encode()).hexdigest()


def sha1(openText: str) -> str:
    """
    Хеширование текста алгоритмом SHA1

    :param openText: открытый текст
    :return: закрытый текст
    """
    return _sha1(openText.encode()).hexdigest()


def hasRight(*, right: RightEnum):
    """
    Проверка пользовательских прав

    :param right: право, которое необходимо у пользователя
    :return: оригинальный метод
    """
    def checkRight(function):
        @wraps(function)
        async def _checkRight(*args, **kwargs):
            from backend.src.entities.users.UserEntity import UserEntity
            user: UserEntity = kwargs.get("user")
            if not user or right not in user.role.rights:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            function(*args, **kwargs)  # вызов оригинального метода
        return _checkRight
    return checkRight


def trimStr(text: str) -> str | None:
    """
    Убрать повторяющиеся пробелы и лишние пробелы с начала и конца строки

    :param text: строка
    :return: отформатированная строка
    """
    if text is None:
        return text
    while "  " in text:
        text = text.replace("  ", " ")
    return text.strip()


def isJwtToken(token):
    """
    Проверка того, что строка является JWT-токеном

    :param token: токен
    :return: признак того, что строка является JWT-токеном
    """
    jwtPattern = re.compile(r'^Bearer [A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$')
    return bool(jwtPattern.match(token))


def validateImage(image: UploadFile) -> bool:
    """
    Валидация загружаемого с формы файла (изображения)

    :param image: изображение
    :return: признак успешного прохождения валидации
    """
    if image.size > MAX_IMG_SIZE_BYTES or not image.content_type.startswith("image/"):
        return False
    return True


def getPaginated(page: int,
                 size: int,
                 query: Query,
                 convert: Callable) -> PaginatedResponse:
    """
    Отформатировать ответ с учётом пагинации

    :param page: необходимая страница
    :param size: необходимое кол-во элементов на странице
    :param query: отфильтрованный запрос
    :param convert: конвертация элементов сущностей в модели для API
    :return: ответ с пагинацией
    """
    totalCount = query.count()
    page = min(totalCount // size + 1, page)
    offset = (page - 1) * size

    query = query.offset(offset).limit(size)

    return PaginatedResponse(
        page=page,
        size=query.count(),
        totalCount=totalCount,
        content=list(map(convert, query.all()))
    )

