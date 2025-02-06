import re
from datetime import datetime
from functools import wraps
from hashlib import sha512 as _sha512
from random import randint
from re import match

from fastapi import HTTPException, status, Request

from backend.src.Constants import EMAIL_PATTERN, LOGIN_PATTERN
from backend.src.exceptions.users.UserAlreadyAuthorizedException import UserAlreadyAuthorizedException
from backend.src.models.enum.RightEnum import RightEnum
from backend.src.models.enum.TemplateEnum import TemplateEnum
from backend.src.models.rest.users.UserModel import UserModel


def generateCode() -> int:
    """
    Генерация одноразового кода

    :return: одноразовый код
    """
    return randint(100000, 999999)


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


def hasRight(*, right: RightEnum):
    """
    Проверка пользовательских прав

    :param right: право, которое необходимо у пользователя
    :return: оригинальный метод
    """
    def checkRight(function):
        @wraps(function)
        async def _checkRight(*args, **kwargs):
            user: UserModel = kwargs.get("user")
            if not user or right not in user.rights:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
            function(*args, **kwargs)  # вызов оригинального метода
        return _checkRight
    return checkRight


def validateEmail(email: str) -> str:
    """
    Валидация адреса электронной почты пользователя при регистрации

    :param email: адрес электронной почты пользователя
    :return: признак успешно пройденной валидации
    """
    if match(EMAIL_PATTERN, email):
        return email
    raise ValueError("WRONG_EMAIL_FORMAT")


def validateUsername(username: str) -> str:
    """
    Валидация имени пользователя при регистрации

    :param username: имя пользователя
    :return: признак успешно пройденной валидации
    """
    if match(LOGIN_PATTERN, username):
        return username
    raise ValueError("WRONG_USERNAME_FORMAT")


def validatePassword(password: str) -> str:
    """
    Валидация пароля пользователя при регистрации

    :param password: пароль пользователя
    :return: признак успешно пройденной валидации
    """
    if password and len(password) >= 8:
        return password
    raise ValueError("WRONG_PASSWORD_FORMAT")


def isJwtToken(token):
    """
    Проверка того, что строка является JWT-токеном

    :param token: токен
    :return: признак того, что строка является JWT-токеном
    """
    jwtPattern = re.compile(r'^Bearer [A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$')
    return bool(jwtPattern.match(token))


def RequireUnauthorized(function):
    @wraps(function)
    async def _checkNotAuthorized(*args, **kwargs):
        request: Request = kwargs.get("request")
        bearerToken = request.headers.get("Authorization")
        if not bearerToken or not isJwtToken(bearerToken):
            return await function(*args, **kwargs)
        try:
            from backend.src.services.users.AuthorizationService import AuthorizationService
            AuthorizationService(kwargs.get("session")).getCurrentUser(bearerToken.split(" ")[-1])
        except Exception:
            return await function(*args, **kwargs)
        raise UserAlreadyAuthorizedException()
    return _checkNotAuthorized
