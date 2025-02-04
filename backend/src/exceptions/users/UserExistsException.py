from fastapi import HTTPException, status


class UserExistsException(HTTPException):
    """
    Исключение, выбрасываемое в случае, если пользователь с введёнными при регистрации данными уже существует
    """
    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT,
                         detail={
                             "type": "USER_ALREADY_EXISTS",
                             "detail": "Пользователь с указанными данными уже существует"
                         })
