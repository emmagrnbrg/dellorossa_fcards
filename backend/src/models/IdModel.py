from pydantic import BaseModel


class IdModel(BaseModel):
    """
    Базовая модель для id
    """
    id: int | str  # id записи
