from enum import StrEnum


class RightEnum(StrEnum):
    """
    Список прав в системе
    """
    EDIT_SETS = "EDIT_SETS"  # право на редактирование (модерацию, публикацию, удаление) наборов карточек
    TEST = "TEST"
