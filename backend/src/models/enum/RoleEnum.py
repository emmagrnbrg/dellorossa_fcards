from enum import StrEnum


class RoleEnum(StrEnum):
    """
    Роли пользователей
    """
    USER = "USER"  # пользователь
    MODERATOR = "MODERATOR"  # модератор
    ADMIN = "ADMIN"  # администратор
