from typing import Annotated

from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.src.Database import getDbSession
from backend.src.models.rest.users.RefreshTokenRequestModel import RefreshTokenRequestModel
from backend.src.models.rest.users.TokenResponseModel import TokenResponseModel
from backend.src.models.rest.users.UserModel import UserModel
from backend.src.services.users.AuthorizationService import AuthorizationService

router = APIRouter()

# аутентификация
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="authenticate", scheme_name="JWT")


async def getCurrentActiveUser(token: str = Depends(oauth2Scheme),
                               session: Session = Depends(getDbSession)) -> UserModel:
    """
    Получить данные текущего авторизованного пользователя

    :param token: токен пользователя
    :param session: сессия соединения с БД
    :return: данные пользователя
    """
    return AuthorizationService(session).getCurrentUser(token)


@router.post("/authenticate")
def login(payload: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(getDbSession)) -> TokenResponseModel:
    """
    Аутентификация пользователя в систему

    :param payload: данные формы для аутентификации
    :param session: сессия соединения с БД
    :return: refresh & access-токены
    """
    return AuthorizationService(session).authenticate(payload.username, payload.password)


@router.get("/user")
def getCurrentUser(user: Annotated[UserModel, Depends(getCurrentActiveUser)]) -> UserModel:
    """
    Получить данные текущего авторизованного пользователя

    :param user: данные пользователя
    :return: данные пользователя
    """
    return user


@router.post("/token/refresh")
async def refreshToken(request: Annotated[RefreshTokenRequestModel, Body()],
                       session: Session = Depends(getDbSession)) -> TokenResponseModel:
    """
    Запрос на обновление access-токена пользователя

    :param request: тело запроса
    :param session: сессия соединения с БД
    :return: access & refresh токены доступа
    """
    return AuthorizationService(session).refreshToken(request.token)
