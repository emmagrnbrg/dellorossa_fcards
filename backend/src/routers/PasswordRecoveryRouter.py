from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session
from starlette.responses import Response

from backend.src.Database import getDbSession
from backend.src.models.UserModel import PasswordRecoveryRequestModel, OperationResponseModel, PasswordResetRequestModel
from backend.src.services.users.PasswordRecoveryService import PasswordRecoveryService

router = APIRouter()


@router.post("/password-recovery")
async def recoveryPassword(requestBody: Annotated[PasswordRecoveryRequestModel, Body()],
                           session: Session = Depends(getDbSession)) -> OperationResponseModel:
    """
    Запрос на восстановление пароля

    :param requestBody: тело запроса
    :param session: сессия соединения с БД
    :return: uuid созданной заявки
    """
    return PasswordRecoveryService(session).recoveryPassword(requestBody.email)


@router.post("/{operationUuid}/reset-password")
async def resetPassword(operationUuid: str,
                        requestBody: Annotated[PasswordResetRequestModel, Body()],
                        session: Session = Depends(getDbSession)) -> Response:
    """
    Запрос на сброс пароля (установление нового)

    :param operationUuid: uuid операции
    :param requestBody: тело запроса
    :param session: сессия соединения с БД
    :return: пустой ответ в случае отсутствия ошибок
    """
    PasswordRecoveryService(session).resetPassword(operationUuid, requestBody)
    return Response()
