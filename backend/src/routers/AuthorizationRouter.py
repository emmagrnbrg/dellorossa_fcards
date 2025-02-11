from typing import Annotated

from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.src.Database import getDbSession
from backend.src.entities.users.UserEntity import UserEntity
from backend.src.models.UserModel import TokenResponseModel, UserModel, RefreshTokenRequestModel
from backend.src.services.users.AuthorizationService import AuthorizationService

router = APIRouter()

# аутентификация
oauth2Scheme = OAuth2PasswordBearer(tokenUrl="authenticate", scheme_name="JWT", auto_error=False)


async def getCurrentActiveUser(token: str | None = Depends(oauth2Scheme),
                               session: Session = Depends(getDbSession)) -> UserEntity:
    """
    Получить данные текущего авторизованного пользователя

    :param token: токен пользователя
    :param session: сессия соединения с БД
    :return: данные пользователя
    """
    return AuthorizationService(session).getCurrentUser(token)


async def getCurrentActiveUserOptional(token: str | None = Depends(oauth2Scheme),
                                       session: Session = Depends(getDbSession)) -> UserEntity | None:
    """
    Опциональная проверка на авторизацию

    :param token: access-токен при наличии
    :param session: сессия соединения с БД
    :return: данные пользователя в случае его авторизации
    """
    if token is None:
        return None
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
def getCurrentUser(user: Annotated[UserEntity, Depends(getCurrentActiveUser)]) -> UserModel:
    """
    Получить данные текущего авторизованного пользователя

    :param user: данные пользователя
    :return: данные пользователя
    """
    return UserModel(id=user.id,
                     email=user.email,
                     username=user.username,
                     role=user.role.name,
                     rights=list(map(lambda right: right.name, user.role.rights)))


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
