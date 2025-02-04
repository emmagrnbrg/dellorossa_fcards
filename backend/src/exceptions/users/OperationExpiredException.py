from fastapi import HTTPException, status


class OperationExpiredException(HTTPException):
    """
    Исключение, выбрасываемое в случае, если время действия операции пользователя истекло
    """
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail={
                             "type": "OPERATION_EXPIRED",
                             "detail": "Операция не найдена или время действия операции истекло"
                         })
