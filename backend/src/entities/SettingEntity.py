from sqlalchemy import Column, Integer, String, Enum

from backend.src.Database import BaseEntity
from backend.src.enums.SettingEnum import SettingEnum


class SettingEntity(BaseEntity):
    """
    Модель данных настройки системы
    """
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Enum(SettingEnum), unique=True, nullable=False)
    value = Column(String, nullable=False)
    description = Column(String, nullable=False)
