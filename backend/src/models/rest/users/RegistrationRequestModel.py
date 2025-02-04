from typing import Annotated

from pydantic import BaseModel, PlainValidator

from backend.src.Utils import validateEmail, validateUsername, validatePassword


class RegistrationRequestModel(BaseModel):
    """
    Модель тела запроса регистрации пользователя
    """
    email: Annotated[str, PlainValidator(validateEmail)]  # адрес электронной почты
    username: Annotated[str, PlainValidator(validateUsername)]  # логин
    password: Annotated[str, PlainValidator(validatePassword)]  # пароль (в открытом виде)
