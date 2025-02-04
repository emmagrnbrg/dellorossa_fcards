from sqlalchemy import Column, Integer, String, Enum

from backend.src.Database import BaseEntity
from backend.src.models.enum.RightEnum import RightEnum


class RightEntity(BaseEntity):
    """
    Модель данных права пользователя (по роли)
    """
    __tablename__ = "rights"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(RightEnum), unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
