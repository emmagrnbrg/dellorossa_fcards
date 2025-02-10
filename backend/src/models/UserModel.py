from re import match
from typing import Annotated

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, PlainValidator, Field

from backend.src.Constants import LOGIN_PATTERN
from backend.src.enums.UsersEnum import RightEnum, RoleEnum


def _validateUsername(username: str) -> str:
    """
    Валидация имени пользователя при регистрации

    :param username: имя пользователя
    :return: признак успешно пройденной валидации
    """
    if match(LOGIN_PATTERN, username):
        return username
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail={
                            "type": "WRONG_USERNAME_FORMAT",
                            "detail": "Имя пользователя должно начинаться с латинского символа, "
                                      "а также содержать латинские символы, цифры и символы нижнего подчеркивания."
                        })


def _validatePassword(password: str) -> str:
    """
    Валидация пароля пользователя при регистрации

    :param password: пароль пользователя
    :return: признак успешно пройденной валидации
    """
    if password and len(password) >= 8:
        return password
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail={
                            "type": "WRONG_PASSWORD_FORMAT",
                            "detail": "Пароль пользователя должен состоять минимум из 8 символов."
                        })


class UserModel(BaseModel):
    """
    Модель данных пользователя
    """
    id: int  # id пользователя
    email: EmailStr  # адрес электронной почты
    username: Annotated[str, PlainValidator(_validateUsername)]  # имя пользователя
    role: RoleEnum  # роль пользователя
    rights: list[RightEnum]  # список прав пользователя


class OperationResponseModel(BaseModel):
    """
    Модель тела ответа на запросы создания операций
    """
    uuid: str  # uuid операции


class PasswordRecoveryRequestModel(BaseModel):
    """
    Модель тела запроса на восстановление пароля
    """
    email: EmailStr  # адрес электронной почты


class PasswordResetRequestModel(BaseModel):
    """
    Модель тела запроса на установление нового пароля
    """
    password: Annotated[str, PlainValidator(_validatePassword)]  # новый пароль пользователя (в открытом виде)
    code: str = Field(min_length=6, max_length=6)  # одноразовый код


class RefreshTokenRequestModel(BaseModel):
    """
    Модель тела запроса на обновление access-токена
    """
    token: str  # refresh-токен


class RegistrationRequestModel(BaseModel):
    """
    Модель тела запроса регистрации пользователя
    """
    email: EmailStr  # адрес электронной почты
    username: Annotated[str, PlainValidator(_validateUsername)]  # логин
    password: Annotated[str, PlainValidator(_validatePassword)]  # пароль (в открытом виде)


class TokenResponseModel(BaseModel):
    """
    Модель тела ответа, содержащего токены доступа (авторизации)
    """
    token_type: str = "Bearer"  # тип токена
    refresh_token: str  # refresh-токен
    access_token: str  # access-токен


class UserShortDataModel(BaseModel):
    """
    Модель основных данных пользователя
    """
    id: int  # id
    username: Annotated[str, PlainValidator(_validateUsername)]  # имя пользователя


class VerifyRegistrationRequestModel(BaseModel):
    """
    Модель тела запроса на верификацию адреса электронной почты (этап окончательной регистрации)
    """
    userData: RegistrationRequestModel  # данные пользователя для регистрации
    oneTimeCode: str = Field(min_length=6, max_length=6)  # одноразовый код из письма
