from sqlalchemy.orm import Session

from backend.src.Utils import isExpired
from backend.src.entities.users.OperationEntity import OperationEntity
from backend.src.enums.UsersEnum import OperationTypeEnum
from backend.src.exceptions.users.IncorrectCodeException import IncorrectCodeException
from backend.src.exceptions.users.OperationExpiredException import OperationExpiredException
from backend.src.services.users.UserService import UserService


class OperationService:
    """
    Сервис операций пользователей
    """
    def __init__(self, session: Session):
        self.__session = session
        self.__userService = UserService(session)

    def create(self, userId: int | None, operationType: OperationTypeEnum) -> OperationEntity:
        """
        Создать пользовательскую операцию

        :param userId: id пользователя (при наличии)
        :param operationType: тип операции
        :return: uuid операции
        """
        operation: OperationEntity = OperationEntity(self.__userService.findById(userId), operationType)
        self.__session.add(operation)
        self.__session.commit()
        return operation

    def verify(self, operationType: OperationTypeEnum, uuid: str, code: str) -> OperationEntity:
        """
        Проверить подлинность введённого одноразового кода

        :param operationType: тип операции
        :param uuid: uuid операции
        :param code: код, введённый пользователем
        :return: данные операции
        """
        operation: OperationEntity | None = self.__session.query(OperationEntity)\
            .filter(OperationEntity.id == uuid)\
            .first()
        if not operation or isExpired(operation.expirationTime) or operation.type != operationType:
            raise OperationExpiredException()
        if operation.code != code:
            raise IncorrectCodeException()

        return operation
