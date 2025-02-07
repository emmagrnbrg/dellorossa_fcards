from fastapi import HTTPException, status


class SetNameValidationException(HTTPException):
    """
    Исключение, выбрасываемое в случае ошибки валидации наименования набора
    """
    def __init__(self):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                         detail={
                             "type": "WRONG_SET_NAME_FORMAT",
                             "detail": "Наименование набора должно быть длиной от 4 до 55 символов, "
                                       "начинаться с буквенного символа и может состоять из кириллических "
                                       "или латинских символов, цифр, пробелов, знаков нижнего подчеркивания (_), "
                                       "знаков решётки (#)"
                         })
