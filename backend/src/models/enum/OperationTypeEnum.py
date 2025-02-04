from enum import StrEnum


class OperationTypeEnum(StrEnum):
    """
    Типы операций пользователей
    """
    PASSWORD_RECOVERY = "PASSWORD_RECOVERY"  # восстановление пароля
    REGISTRATION = "REGISTRATION"  # регистрация
