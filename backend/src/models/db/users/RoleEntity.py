from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship

from backend.src.Database import BaseEntity
from backend.src.models.db.users.RightEntity import RightEntity
from backend.src.models.db.users.RoleRightEntity import RoleRightEntity
from backend.src.models.enum.RoleEnum import RoleEnum


class RoleEntity(BaseEntity):
    """
    Модель данных роли пользователя
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="id роли")
    type = Column(Enum(RoleEnum), nullable=False, comment="Тип роли")
    name = Column(String, nullable=False, comment="Наименование роли")
    rights = relationship("RightEntity", secondary=RoleRightEntity)
