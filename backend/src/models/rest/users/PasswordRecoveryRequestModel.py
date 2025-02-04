from typing import Annotated

from pydantic import BaseModel, PlainValidator

from backend.src.Utils import validateEmail


class PasswordRecoveryRequestModel(BaseModel):
    """
    Модель тела запроса на восстановление пароля
    """
    email: Annotated[str, PlainValidator(validateEmail)]  # адрес электронной почты
