from pydantic import BaseModel


class OperationResponseModel(BaseModel):
    """
    Модель тела ответа на запросы создания операций
    """
    uuid: str  # uuid операции
