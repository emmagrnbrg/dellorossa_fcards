from fastapi import HTTPException, status


class UserException(HTTPException):
    """
    Исключение, выбрасываемое в случае, если произошла ошибка при получении данных пользователя
    """
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT,
                         detail={
                             "type": "USER_EXCEPTION",
                             "detail": "Произошла ошибка при получении данных пользователя"
                         })
