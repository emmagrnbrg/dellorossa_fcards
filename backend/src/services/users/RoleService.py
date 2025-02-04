from sqlalchemy.orm import Session

from backend.src.models.db.users.RoleEntity import RoleEntity
from backend.src.models.enum.RoleEnum import RoleEnum


class RoleService:
    """
    Сервис ролей
    """
    def __init__(self, session: Session):
        self.__session = session

    def getUser(self) -> RoleEntity | None:
        """
        Получить роль обычного пользователя системы

        :return: роль обычного пользователя системы
        """
        return self.__getRole(RoleEnum.USER)

    def __getRole(self, roleType: RoleEnum) -> RoleEntity | None:
        """
        Получить роль пользователя по типу

        :param roleType: тип роли
        :return: роль пользователя
        """
        return self.__session.query(RoleEntity).filter(RoleEntity.type == roleType).first()
