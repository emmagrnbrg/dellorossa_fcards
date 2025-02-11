from sqlalchemy import Integer, Column, Table, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.src.Database import BaseEntity
from backend.src.entities.users.UserEntity import UserEntity
from backend.src.entities.sets.SetEntity import SetEntity


class SetGradeEntity(BaseEntity):
    """
    Оценки, проставляемые пользователями наборам
    """
    __tablename__ = "set_grades"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, comment="id записи")
    setId = Column("set_id", String, ForeignKey("sets.id"), nullable=False)
    graderId = Column("grader_id", Integer, ForeignKey("users.id"), nullable=False)
    grade = Column("grade", Integer, comment="Оценка", nullable=False)

    grader = relationship("UserEntity", backref="sets_grades")
    set = relationship("SetEntity", backref="sets_grades")

    def __init__(self, setEntity: SetEntity, graderEntity: UserEntity, grade: int = 0):
        self.setId = setEntity.id
        self.graderId = graderEntity.id
        self.grade = grade

        self.set = setEntity
        self.grader = graderEntity

