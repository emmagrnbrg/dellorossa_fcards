from fastapi import HTTPException, status


class UserNotExistsException(HTTPException):
    """
    Исключение, выбрасываемое в случае, если пользователь не существует
    """
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT,
                         detail={
                             "type": "USER_NOT_EXISTS",
                             "detail": "Пользователь с указанным адресом электронной почты не найден"
                         })
