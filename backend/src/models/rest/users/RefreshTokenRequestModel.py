from pydantic import BaseModel


class RefreshTokenRequestModel(BaseModel):
    """
    Модель тела запроса на обновление access-токена
    """
    token: str  # refresh-токен
