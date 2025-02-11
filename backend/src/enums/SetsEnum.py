import datetime
from enum import StrEnum


class AccessEnum(StrEnum):
    """
    Модификаторы доступа наборов
    """
    PRIVATE = "PRIVATE"  # приватный
    LINK_RESTRICTED = "LINK_RESTRICTED"  # доступ по ссылке
    USER_RESTRICTED = "USER_RESTRICTED"  # доступ определенной группе пользователей
    PUBLIC = "PUBLIC"  # публичный


class SetDateFilterEnum(StrEnum):
    """
    Модель фильтрации по дате
    """
    WEEK = "WEEK"  # последняя неделя
    MONTH = "MONTH"  # последний месяц
    YEAR = "YEAR"  # последний год
    ALL_TIME = "ALL_TIME"  # всё время

    def getStartFrom(self) -> datetime.date | None:
        today = datetime.date.today()
        if self.value == SetDateFilterEnum.WEEK:
            delta = 7
        elif self.value == SetDateFilterEnum.MONTH:
            delta = 30
        elif self.value == SetDateFilterEnum.YEAR:
            delta = 365
        else:
            return None
        return today - datetime.timedelta(days=delta)


class SetSortEnum(StrEnum):
    """
    Модель сортировки наборов
    """
    NEWEST_FIRST = "NEWEST_FIRST"  # новые
    BY_HIGHEST_GRADE = "BY_HIGHEST_GRADE"  # с наивысшей оценкой
    POPULAR_FIRST = "POPULAR_FIRST"  # популярные
