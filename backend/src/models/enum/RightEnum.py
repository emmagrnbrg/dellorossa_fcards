from enum import StrEnum


class RightEnum(StrEnum):
    """
    Список прав в системе
    """
    VIEW_ALL_SETS = "VIEW_ALL_SETS"  # просмотр всех наборов (включая приватные)
    EDIT_SETS = "EDIT_SETS"  # право на редактирование (модерацию, публикацию, удаление) ПУБЛИЧНЫХ наборов карточек
