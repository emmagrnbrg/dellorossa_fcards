import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Date, BLOB
from sqlalchemy.orm import relationship

from backend.src.Database import BaseEntity
from backend.src.Utils import sha1
from backend.src.models.db.cards.SetMemberEntity import SetMemberEntity
from backend.src.models.enum.AccessEnum import AccessEnum
from backend.src.models.db.users.UserEntity import UserEntity
from backend.src.models.db.cards.CardEntity import CardEntity


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

    owner = relationship("UserEntity", backref="sets")
    cards = relationship("CardEntity", uselist=True, backref="sets")
    members = relationship("UserEntity", secondary=SetMemberEntity)

    def __init__(self, name: str, description: str | None, owner: UserEntity):
        __currentTime = datetime.datetime.now()

        self.id = sha1("{}_{}_{}".format(str(__currentTime), owner.username, name))
        self.name = name
        self.description = description
        self.owner = owner
        self.ownerId = owner.id
        # self.access = AccessEnum.PRIVATE
        # self.creationDate = __currentTime.date()
        # self.modificationDate = __currentTime.date()
