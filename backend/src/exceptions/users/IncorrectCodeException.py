from fastapi import HTTPException, status


class IncorrectCodeException(HTTPException):
    """
    Исключение, выбрасываемое в случае, если введённый одноразовый код неверный
    """
    def __init__(self):
        super().__init__(status_code=status.HTTP_417_EXPECTATION_FAILED,
                         detail={
                             "type": "INCORRECT_ONE_TIME_CODE",
                             "detail": "Одноразовый код введён неверно"
                         })
