import pathlib
from enum import StrEnum

_BASE_TEMPLATE_PATH = f"{str(pathlib.Path(__file__).parents[1])}\\static\\email-templates\\"


class TemplateEnum(StrEnum):
    """
    Список шаблонов электронных писем
    """
    RECOVERY_PASSWORD = _BASE_TEMPLATE_PATH + "RecoveryPassword.html"
    REGISTRATION = _BASE_TEMPLATE_PATH + "RegistrationVerify.html"
