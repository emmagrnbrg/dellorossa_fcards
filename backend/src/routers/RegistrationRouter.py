from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from backend.src.Database import getDbSession
from backend.src.models.rest.users.OperationResponseModel import OperationResponseModel
from backend.src.models.rest.users.RegistrationRequestModel import RegistrationRequestModel
from backend.src.models.rest.users.VerifyRegistrationRequestModel import VerifyRegistrationRequestModel
from backend.src.services.users.RegistrationService import RegistrationService

router = APIRouter(prefix="/registration")


@router.post("/create")
async def register(request: Annotated[RegistrationRequestModel, Body()],
                   session: Session = Depends(getDbSession)) -> OperationResponseModel:
    """
    Запрос на создание заявки на регистрацию пользователя

    :param request: тело запроса
    :param session: сессия для соединения с БД
    :return: uuid созданной заявки
    """
    return RegistrationService(session).register(request)


@router.post("/{operationUuid}/verify")
async def verify(operationUuid: str,
                 request: Annotated[VerifyRegistrationRequestModel, Body()],
                 session: Session = Depends(getDbSession)):
    """
    Запрос на верификацию адреса электронной почты - окончание этапа регистрации

    :param operationUuid: uuid заявки
    :param request: тело запроса
    :param session: сессия для соединения с БД
    :return: пустой ответ в случае отсутствия ошибок
    """
    RegistrationService(session).verify(operationUuid, request)
