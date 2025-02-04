from pydantic import BaseModel

from backend.src.models.enum.RightEnum import RightEnum


class UserModel(BaseModel):
    """
    Модель данных пользователя
    """
    id: int  # id пользователя
    email: str  # адрес электронной почты
    username: str  # имя пользователя
    role: str  # роль пользователя
    rights: list[RightEnum]  # список прав пользователя
