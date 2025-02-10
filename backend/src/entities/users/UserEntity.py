from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.src.Database import BaseEntity
from backend.src.Utils import sha512
from backend.src.entities.users.RoleEntity import RoleEntity


class UserEntity(BaseEntity):
    """
    Модель данных пользователя
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="id пользователя")
    email = Column(String, unique=True, index=True, nullable=False, comment="Адрес электронной почты пользователя")
    username = Column(String, unique=True, index=True, nullable=False, comment="Имя пользователя")
    roleId = Column("role_id", Integer, ForeignKey("roles.id"), comment="id роли пользователя")
    password = Column(String, nullable=False, comment="Пароль пользователя (в закрытом виде)")

    role = relationship("RoleEntity", backref="users")

    def __init__(self, email: str, username: str, role: RoleEntity, password: str):
        self.email = email
        self.username = username
        self.role = role
        self.roleId = role.id
        self.password = sha512(password)
