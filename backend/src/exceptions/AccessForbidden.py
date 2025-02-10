from fastapi import HTTPException, status


class AccessForbidden(HTTPException):
    """
    Исключение, выбрасываемое в случае, если набор карточек не найден / не доступен
    """
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN,
                         detail={
                             "type": "ACCESS_FORBIDDEN",
                             "detail": "Нет доступа для выполнения данной операции"
                         })
