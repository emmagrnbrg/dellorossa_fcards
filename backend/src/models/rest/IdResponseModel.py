from pydantic import BaseModel


class IdResponseModel(BaseModel):
    """
    Базовая модель ответа, содержащая id записи
    """
    id: int | str  # id записи
