import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy.orm import Session

from backend.src.services.SettingsService import SettingsService


class EmailService:
    """
    Сервис отправки электронных писем
    """
    def __init__(self, session: Session):
        self.__settingService = SettingsService(session)

        self.__from = self.__settingService.getEmailLogin()
        self.__server = smtplib.SMTP_SSL(self.__settingService.getEmailHost(),
                                         self.__settingService.getEmailPort())
        self.__server.login(self.__from, self.__settingService.getEmailPassword())

    def send(self, to: str, topic: str, body: str) -> None:
        """
        Отправка электронного письма

        :param to: адресат письма
        :param topic: тема письма
        :param body: тело письма
        """
        msg = MIMEMultipart()
        msg["From"] = self.__from
        msg["To"] = to
        msg["Subject"] = topic

        msg.attach(MIMEText(body, "html"))

        self.__server.sendmail(self.__from, to, msg.as_string())
        self.__server.close()
