from enum import StrEnum


class AccessEnum(StrEnum):
    """
    Модификаторы доступа наборов
    """
    PRIVATE = "PRIVATE"  # приватный
    LINK_RESTRICTED = "LINK_RESTRICTED"  # доступ по ссылке
    USER_RESTRICTED = "USER_RESTRICTED"  # доступ определенной группе пользователей
    PUBLIC = "PUBLIC"  # публичный
