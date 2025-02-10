from enum import StrEnum


class OperationTypeEnum(StrEnum):
    """
    Типы операций пользователей
    """
    PASSWORD_RECOVERY = "PASSWORD_RECOVERY"  # восстановление пароля
    REGISTRATION = "REGISTRATION"  # регистрация


class RoleEnum(StrEnum):
    """
    Роли пользователей
    """
    USER = "USER"  # пользователь
    MODERATOR = "MODERATOR"  # модератор
    ADMIN = "ADMIN"  # администратор


class RightEnum(StrEnum):
    """
    Список прав в системе
    """
    VIEW_ALL_SETS = "VIEW_ALL_SETS"  # просмотр всех наборов (включая приватные)
    EDIT_SETS = "EDIT_SETS"  # право на редактирование (модерацию, публикацию, удаление) ПУБЛИЧНЫХ наборов карточек
