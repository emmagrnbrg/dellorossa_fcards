from fastapi import HTTPException, status


class AuthenticationException(HTTPException):
    """
    Исключение, выбрасываемое в случае, если произошла ошибка при аутентификации (не совпадает e-mail / пароль)
    """
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail={
                             "type": "AUTHENTICATION_FAILED",
                             "detail": "Пользователь с указанным e-mail не найден или пароль введён неверно"
                         })
