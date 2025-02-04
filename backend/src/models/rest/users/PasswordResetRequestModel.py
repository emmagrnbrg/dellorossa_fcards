from typing import Annotated

from pydantic import BaseModel, PlainValidator

from backend.src.Utils import validatePassword


class PasswordResetRequestModel(BaseModel):
    """
    Модель тела запроса на установление нового пароля
    """
    password: Annotated[str, PlainValidator(validatePassword)]  # новый пароль пользователя (в открытом виде)
    code: int  # одноразовый код
