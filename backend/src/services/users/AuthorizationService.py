from datetime import datetime, timedelta

from jose import jwt, JWTError
from sqlalchemy.orm import Session

from backend.src.Constants import REFRESH_TOKEN_LIFETIME_MINUTES, ACCESS_TOKEN_LIFETIME_MINUTES
from backend.src.Utils import sha512, isExpired
from backend.src.entities.users.UserEntity import UserEntity
from backend.src.exceptions.users.AuthenticationException import AuthenticationException
from backend.src.exceptions.users.SessionExpiredException import SessionExpiredException
from backend.src.exceptions.users.UserException import UserException
from backend.src.models.UserModel import TokenResponseModel
from backend.src.services.SettingsService import SettingsService
from backend.src.services.users.UserService import UserService


class AuthorizationService:
    """
    Сервис авторизации пользователей
    """

    def __init__(self, session: Session):
        self.__session = session
        self.__settingService = SettingsService(session)
        self.__userService = UserService(session)

    def authenticate(self, email: str, password: str) -> TokenResponseModel:
        """
        Аутентификация пользователя

        :param email: адрес электронной почты
        :param password: пароль
        :return: токены доступа
        """
        user: UserEntity = self.__userService.findByEmail(email)
        if not user or sha512(password) != user.password:
            raise AuthenticationException()
        return TokenResponseModel(refresh_token=self.__generateToken(user.id, REFRESH_TOKEN_LIFETIME_MINUTES),
                                  access_token=self.__generateToken(user.id, ACCESS_TOKEN_LIFETIME_MINUTES))

    def getCurrentUser(self, token: str) -> UserEntity:
        """
        Получить данные текущего авторизованного пользователя

        :param token: токен пользователя
        :return: текущий пользователь
        """
        return self.__checkToken(token)

    def refreshToken(self, refreshToken: str) -> TokenResponseModel:
        """
        Обновить refresh-токен

        :param refreshToken: текущий refresh-токен
        :return: обновлённые токены
        """
        user = self.__checkToken(refreshToken)
        return TokenResponseModel(refresh_token=self.__generateToken(user.id, REFRESH_TOKEN_LIFETIME_MINUTES),
                                  access_token=self.__generateToken(user.id, ACCESS_TOKEN_LIFETIME_MINUTES))

    def __checkToken(self, token: str) -> UserEntity | None:
        """
        Проверка валидности токена

        :param token: токен
        :return: данные пользователя, если токен валидный
        """
        try:
            userData = jwt.decode(token,
                                  self.__settingService.getAccessTokenSecretKey(),
                                  algorithms=[self.__settingService.getAccessTokenAlgorithm()])
        except Exception:
            raise UserException()

        userId, expireTime = userData.get("userId"), userData.get("expireTime")
        if not userId or not expireTime:
            raise UserException()

        user: UserEntity | None = self.__userService.findById(userId)
        if not user:
            raise UserException()

        if isExpired(datetime.fromtimestamp(expireTime)):
            raise SessionExpiredException()

        return user

    def __generateToken(self, userId: int, expireIn: int) -> str:
        """
        Генерация токена

        :param userId: идентификатор пользователя
        :param expireIn: время жизни (в минутах)
        :return: сгенерированный токен
        """
        toEncode = {
            "userId": userId,
            "expireTime": round((datetime.now() + timedelta(minutes=expireIn)).timestamp(), 3)
        }
        return jwt.encode(toEncode,
                          self.__settingService.getAccessTokenSecretKey(),
                          algorithm=self.__settingService.getAccessTokenAlgorithm())
