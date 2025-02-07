from fastapi import HTTPException, status


class SetNotFoundException(HTTPException):
    """
    Исключение, выбрасываемое в случае, если набор карточек не найден / не доступен
    """
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND,
                         detail={
                             "type": "SET_NOT_FOUND",
                             "detail": "Набор карточек не найден или не доступен"
                         })
