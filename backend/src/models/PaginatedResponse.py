from pydantic import BaseModel


class PaginatedResponse(BaseModel):
    """
    Ответ для запроса с пагинацией
    """
    page: int  # номер страницы
    size: int  # количество элементов на странице
    totalCount: int  # общее количество элементов
    content: list  # содержимое страницы
