from pydantic import BaseModel

from backend.src.models.rest.users.RegistrationRequestModel import RegistrationRequestModel


class VerifyRegistrationRequestModel(BaseModel):
    """
    Модель тела запроса на верификацию адреса электронной почты (этап окончательной регистрации)
    """
    userData: RegistrationRequestModel  # данные пользователя для регистрации
    oneTimeCode: int  # одноразовый код из письма
