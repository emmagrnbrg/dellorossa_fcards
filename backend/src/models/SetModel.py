from re import fullmatch
from typing import Annotated

from pydantic import BaseModel, PlainValidator, Field

from backend.src.Constants import SET_NAME_PATTERN
from backend.src.Utils import trimStr
from backend.src.enums.SetsEnum import AccessEnum, SetDateFilterEnum, SetSortEnum
from backend.src.exceptions.cards.SetNameValidationException import SetNameValidationException
from backend.src.models.UserModel import UserShortDataModel


def _validateSetName(name: str) -> str:
    """
    Валидация наименования набора

    :param name: наименование набора
    :return: наименование набора при успешном прохождении валидации
    """
    if not name:
        raise SetNameValidationException()
    name = trimStr(name)
    if not fullmatch(SET_NAME_PATTERN, name):
        raise SetNameValidationException()
    return name


class BaseSetModel(BaseModel):
    """
    Базовая модель для создания / редактирования набора карточек
    """
    name: Annotated[str, PlainValidator(_validateSetName)]  # наименование набора
    description: Annotated[str | None, PlainValidator(trimStr)]  # описание набора
    access: AccessEnum = AccessEnum.PRIVATE  # тип доступа
    userIds: list[int]  # идентификаторы пользователей в случае USER_RESTRICTED


class FilterRequest(BaseModel):
    """
    Запрос для фильтрации табличного просмотра наборов
    """
    name: Annotated[str | None, PlainValidator(trimStr)]  # наименование набора
    dateFilter: SetDateFilterEnum = SetDateFilterEnum.ALL_TIME  # тип фильтрации по дате
    sort: SetSortEnum = SetSortEnum.POPULAR_FIRST  # сортировка наборов
    mine: bool  # отображать наборы только текущего авторизованного пользователя


class TileSetResponse(BaseModel):
    """
    Запрос для отображения наборов в виде плиток
    """
    id: str  # id набора
    name: str  # наименование набора
    author: UserShortDataModel  # данные автора
    description: str | None  # описание
    modificationDate: str  # дата модификации
    cardsAmount: int  # количество карточек в наборе
    grade: float  # оценка
    favoritesCount: int  # количество пользователей, добавивших набор в список избранного


class SetGradeRequestModel(BaseModel):
    """
    Модель тела запроса проставления оценки набору
    """
    grade: int = Field(le=5, ge=1)
