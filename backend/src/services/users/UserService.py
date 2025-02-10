from sqlalchemy import or_
from sqlalchemy.orm import Session

from backend.src.Utils import sha512
from backend.src.entities.users.UserEntity import UserEntity
from backend.src.enums.UsersEnum import RightEnum


class UserService:
    """
    Сервис работы с данными пользователей
    """
    def __init__(self, session: Session):
        self.__session = session

    def findById(self, userId: int) -> UserEntity | None:
        """
        Найти пользователя по id

        :param userId: id пользователя
        :return: данные пользователя
        """
        return self.__session.query(UserEntity).filter(UserEntity.id == userId).first()

    def existsByEmailOrUsername(self, email: str, username: str) -> bool:
        """
        Проверить пользователя на существование по адресу электронной почты или имени пользователя

        :param email: адрес электронной почты
        :param username: имя пользователя
        :return: признак существования пользователя
        """
        return self.__session.query(UserEntity)\
            .filter(or_(UserEntity.username == username, UserEntity.email == email))\
            .first() is not None

    def findByEmail(self, email: str) -> UserEntity | None:
        """
        Найти пользователя по адресу электронной почты

        :param email: адрес электронной почты
        :return: данные пользователя
        """
        return self.__session.query(UserEntity).filter(UserEntity.email == email).first()

    def changePassword(self, user: UserEntity, password: str) -> None:
        """
        Обновить пароль пользователя

        :param user: данные пользователя
        :param password: новый пароль
        :return: пустое тело в случае отсутствия ошибок
        """
        user.password = sha512(password)
        self.__session.add(user)
        self.__session.commit()

    @staticmethod
    def hasRight(user: UserEntity, right: RightEnum) -> bool:
        """
        Проверить, есть ли у пользователя указанное право

        :param user: пользователь
        :param right: право для проверки
        :return: наличие у пользователя указанного права
        """
        return right in list(map(lambda _right: _right.name, user.role.rights))
