from sqlalchemy.orm import Session

from backend.src.Utils import readEmailTemplate
from backend.src.entities.users.OperationEntity import OperationEntity
from backend.src.entities.users.UserEntity import UserEntity
from backend.src.enums.TemplateEnum import TemplateEnum
from backend.src.enums.UsersEnum import OperationTypeEnum
from backend.src.exceptions.users.UserNotExistsException import UserNotExistsException
from backend.src.models.UserModel import OperationResponseModel, PasswordResetRequestModel
from backend.src.services.EmailService import EmailService
from backend.src.services.users.OperationService import OperationService
from backend.src.services.users.UserService import UserService


class PasswordRecoveryService:
    """
    Сервис восстановления паролей пользователей
    """
    def __init__(self, session: Session):
        self.session = session
        self.__userService = UserService(session)
        self.__operationService = OperationService(session)
        self.__emailService = EmailService(session)

    def recoveryPassword(self, email: str) -> OperationResponseModel:
        """
        Восстановить пароль пользователя

        :param email: адрес электронной почты
        :return: идентификатор созданной заявки
        """
        user: UserEntity = self.__userService.findByEmail(email)
        if not user:
            raise UserNotExistsException()

        operation: OperationEntity = OperationEntity(user, OperationTypeEnum.PASSWORD_RECOVERY)
        self.session.add(operation)
        self.session.commit()

        self.__emailService.send(email,
                                 "Восстановление пароля на портале F-cards",
                                 readEmailTemplate(TemplateEnum.RECOVERY_PASSWORD)
                                 .format(code=operation.code))

        return OperationResponseModel(uuid=operation.id)

    def resetPassword(self, operationUuid: str, request: PasswordResetRequestModel) -> None:
        """
        Сброс пароля пользователем

        :param operationUuid: uuid операции по восстановлению пароля
        :param request: данные запроса
        :return: пустое тело ответа в случае отсутствия ошибок
        """
        operation: OperationEntity = self.__operationService.verify(OperationTypeEnum.PASSWORD_RECOVERY,
                                                                    operationUuid,
                                                                    request.code)
        self.__userService.changePassword(operation.user, request.password)
