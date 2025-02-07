from re import fullmatch, match
from typing import Annotated

from pydantic import BaseModel, PlainValidator

from backend.src.Constants import SET_NAME_PATTERN
from backend.src.Utils import trimStr
from backend.src.exceptions.cards.SetNameValidationException import SetNameValidationException


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


class UpdateSetRequestModel(BaseModel):
    """
    Запрос на создание / обновление набора
    """
    name: Annotated[str, PlainValidator(_validateSetName)]  # наименование набора
    description: Annotated[str, PlainValidator(trimStr)]  # описание набора
