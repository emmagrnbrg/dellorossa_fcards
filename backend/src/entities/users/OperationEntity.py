import uuid
from datetime import datetime, timedelta

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from backend.src.Constants import OPERATION_LIFETIME_MIN
from backend.src.Database import BaseEntity
from backend.src.Utils import generateCode
from backend.src.enums.UsersEnum import OperationTypeEnum
from backend.src.entities.users.UserEntity import UserEntity


class OperationEntity(BaseEntity):
    """
    Модель данных операции
    """
    __tablename__ = "operations"

    id = Column(String, primary_key=True, comment="uuid процесса")
    userId = Column("user_id", Integer, ForeignKey("users.id"), comment="id пользователя, инициировавшего процесс")
    expirationTime = Column("expiration_time", DateTime, nullable=False,
                            comment="Время истечения срока действия операции")
    type = Column(Enum(OperationTypeEnum), nullable=False, comment="Тип операции")
    code = Column(String, nullable=False, comment="Одноразовый код подтверждения")

    user = relationship("UserEntity", backref="operations")

    def __init__(self, user: UserEntity, operationType: OperationTypeEnum):
        self.id = str(uuid.uuid4())
        self.user = user
        self.userId = user.id if user else None
        self.type = operationType
        self.expirationTime = datetime.now() + timedelta(minutes=OPERATION_LIFETIME_MIN)
        self.code = generateCode()
