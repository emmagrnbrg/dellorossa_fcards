from sqlalchemy.orm import Session

from backend.src.Utils import readEmailTemplate
from backend.src.entities.users.OperationEntity import OperationEntity
from backend.src.entities.users.UserEntity import UserEntity
from backend.src.enums.TemplateEnum import TemplateEnum
from backend.src.enums.UsersEnum import OperationTypeEnum
from backend.src.exceptions.users.UserExistsException import UserExistsException
from backend.src.models.UserModel import RegistrationRequestModel, OperationResponseModel, \
    VerifyRegistrationRequestModel
from backend.src.services.EmailService import EmailService
from backend.src.services.users.OperationService import OperationService
from backend.src.services.users.RoleService import RoleService
from backend.src.services.users.UserService import UserService


class RegistrationService:
    """
    Сервис регистрации пользователей
    """

    def __init__(self, session: Session):
        self.__session = session
        self.__operationService = OperationService(session)
        self.__roleService = RoleService(session)
        self.__userService = UserService(session)
        self.__emailService = EmailService(session)

    def register(self, request: RegistrationRequestModel) -> OperationResponseModel:
        """
        Создание заявки на регистрацию пользователя

        :param request: тело запроса
        :return: uuid заявки
        """
        self._checkIfUserExists(request.email, request.username)
        operation: OperationEntity = self.__operationService.create(None, OperationTypeEnum.REGISTRATION)
        self.__emailService.send(request.email,
                                 "Регистрация на портале F-cards",
                                 readEmailTemplate(TemplateEnum.REGISTRATION)
                                 .format(code=operation.code))
        return OperationResponseModel(uuid=operation.id)

    def verify(self, operationUuid: str, request: VerifyRegistrationRequestModel) -> None:
        """
        Верификация адреса электронной почты

        :param operationUuid: uuid заявки
        :param request: запрос на регистрацию клиента
        """
        self.__operationService.verify(OperationTypeEnum.REGISTRATION, operationUuid, request.oneTimeCode)
        self._checkIfUserExists(request.userData.email, request.userData.username)
        userEntity: UserEntity = UserEntity(request.userData.email,
                                            request.userData.username,
                                            self.__roleService.getUser(),
                                            request.userData.password)
        self.__session.add(userEntity)
        self.__session.commit()

    def _checkIfUserExists(self, email: str, username: str) -> None:
        """
        Проверка существования пользователя по логину или адресу электронной почты

        :param email: адрес электронной почты
        :param username: имя пользователя
        """
        if self.__userService.existsByEmailOrUsername(email, username):
            raise UserExistsException()
