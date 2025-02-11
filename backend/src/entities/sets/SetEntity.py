import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date, BLOB, Float
from sqlalchemy.orm import relationship

from backend.src.Database import BaseEntity
from backend.src.Utils import sha1
from backend.src.entities.sets.FavoriteSetEntity import FavoriteSetEntity
from backend.src.entities.sets.SetMemberEntity import SetMemberEntity
from backend.src.entities.users.UserEntity import UserEntity
from backend.src.enums.SetsEnum import AccessEnum
from backend.src.entities.cards.CardEntity import CardEntity


class SetEntity(BaseEntity):
    """
    Наборы карточек
    """
    __tablename__ = "sets"

    id = Column(String, primary_key=True, unique=True, nullable=False, comment="id набора")
    name = Column(String, nullable=False, comment="Наименование набора")
    description = Column(String, comment="Описание набора")
    ownerId = Column("owner_id", Integer, ForeignKey("users.id"), nullable=False, comment="id автора")
    bg = Column(BLOB, comment="Метаданные фонового изображения")
    access = Column(Enum(AccessEnum), nullable=False, default=AccessEnum.PRIVATE, comment="Модификатор доступа набора")
    creationDate = Column("creation_date", Date, nullable=False,
                          default=datetime.date.today(), comment="Дата создания набора")
    modificationDate = Column("modification_date", Date, nullable=False,
                              default=datetime.date.today(), comment="Дата модификации набора")
    averageScore = Column("average_score", Float, default=0.0, comment="Средняя оценка")

    owner = relationship("UserEntity", backref="sets")
    cards = relationship("CardEntity", uselist=True, backref="sets")
    grades = relationship("SetGradeEntity", uselist=True, backref="sets")
    members = relationship("UserEntity", secondary=SetMemberEntity)
    favorites = relationship("UserEntity", secondary=FavoriteSetEntity)

    def __init__(self,
                 name: str,
                 description: str | None,
                 owner: UserEntity,
                 members: list[UserEntity],
                 access: AccessEnum = AccessEnum.PRIVATE):
        __currentTime = datetime.datetime.now()

        self.id = sha1("{}_{}_{}".format(str(__currentTime), owner.username, name))
        self.name = name
        self.description = description
        self.owner = owner
        self.ownerId = owner.id
        self.access = access

        if self.access == AccessEnum.USER_RESTRICTED:
            self.members = members
