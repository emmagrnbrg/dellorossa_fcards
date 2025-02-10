from sqlalchemy import Column, Integer, String, ForeignKey

from backend.src.Database import BaseEntity


class CardEntity(BaseEntity):
    """
    Флеш-карточки
    """
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False, comment="id карточки")
    setId = Column("set_id", Integer, ForeignKey("sets.id"), nullable=False, comment="id набора")
    title = Column(String, nullable=False, comment="Текст на лицевой стороне карточки")
    hint = Column(String, comment="Подсказка к карточке")
    description = Column(String, nullable=False, comment="Текст на оборотной стороне карточки")
