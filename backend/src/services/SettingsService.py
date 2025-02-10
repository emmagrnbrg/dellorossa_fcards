from sqlalchemy.orm import Session

from backend.src.entities.SettingEntity import SettingEntity
from backend.src.enums.SettingEnum import SettingEnum


class SettingsService:
    """
    Сервис настроек
    """
    def __init__(self, session: Session):
        self.session = session

    def getAccessTokenSecretKey(self) -> str:
        return self.__get(SettingEnum.ACCESS_TOKEN_SECRET_KEY)

    def getAccessTokenAlgorithm(self) -> str:
        return self.__get(SettingEnum.ACCESS_TOKEN_ALGORITHM)

    def getProcessExpireMinutes(self) -> int:
        """
        Получить значение настройки времени жизни процесса

        :return: время жизни процесса
        """
        return self.__getInteger(SettingEnum.PROCESS_EXPIRE_MINUTES)

    def getHost(self) -> str:
        """
        Получить базовый url приложения

        :return: базовый url приложения
        """
        return self.__get(SettingEnum.PRESENTATION_ORIGIN_HOST)

    def getEmailHost(self) -> str:
        """
        Получить IP-адрес SMTP-сервера для отправки электронных писем

        :return: IP-адрес SMTP-сервера для отправки электронных писем
        """
        return self.__get(SettingEnum.EMAIL_SMTP_HOST)

    def getEmailPort(self) -> int:
        """
        Получить порт SMTP-сервера для отправки электронных писем

        :return: порт SMTP-сервера для отправки электронных писем
        """
        return self.__getInteger(SettingEnum.EMAIL_SMTP_PORT)

    def getEmailLogin(self) -> str:
        """
        Получить логин аккаунта SMTP-сервера для отправки электронных писем

        :return: логин аккаунта SMTP-сервера для отправки электронных писем
        """
        return self.__get(SettingEnum.EMAIL_SMTP_LOGIN)

    def getEmailPassword(self) -> str:
        """
        Получить пароль аккаунта SMTP-сервера для отправки электронных писем

        :return: пароль аккаунта SMTP-сервера для отправки электронных писем
        """
        return self.__get(SettingEnum.EMAIL_SMTP_PASSWORD)

    def __getInteger(self, name: SettingEnum) -> int:
        """
        Получить значение настройки, представляющее целое число

        :param name: наименование настройки (ключ)
        :return: целочисленное значение настройки
        """
        return int(self.__get(name))

    def __get(self, name: SettingEnum) -> str:
        """
        Получить значение настройки

        :param name: наименование настройки (ключ)
        :return: значение настройки
        """
        return self.session.query(SettingEntity).filter(SettingEntity.name == name).first().value
