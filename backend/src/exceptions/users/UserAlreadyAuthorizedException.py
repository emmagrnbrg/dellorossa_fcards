from fastapi import HTTPException, status


class UserAlreadyAuthorizedException(HTTPException):
    """
    Исключение, выбрасываемое в случае, если пользователь уже авторизован
    (а метод не должен быть доступен для авторизованных пользователей)
    """
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN,
                         detail={
                             "type": "USER_ALREADY_AUTHORIZED",
                             "detail": "Вызываемый ресурс недоступен для авторизованных пользователей. "
                                       "Выйдите из системы и повторите заново"
                         })
