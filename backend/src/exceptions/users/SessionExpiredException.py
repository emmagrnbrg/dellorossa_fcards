from fastapi import HTTPException, status


class SessionExpiredException(HTTPException):
    """
    Исключение, выбрасываемое в случае, если пользовательская сессия истекла
    """
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail={
                             "type": "SESSION_EXPIRED",
                             "detail": "Сессия истекла. Пожалуйста, авторизуйтесь заново"
                         })
