from pydantic import BaseModel


class TokenResponseModel(BaseModel):
    """
    Модель тела ответа, содержащего токены доступа (авторизации)
    """
    token_type: str = "Bearer"  # тип токена
    refresh_token: str  # refresh-токен
    access_token: str  # access-токен
