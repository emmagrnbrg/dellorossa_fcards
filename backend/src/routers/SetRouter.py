from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends, Body, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import Response

from backend.src.Database import getDbSession
from backend.src.Utils import validateImage
from backend.src.models.db.users.UserEntity import UserEntity
from backend.src.models.rest.IdResponseModel import IdResponseModel
from backend.src.models.rest.cards.UpdateSetRequestModel import UpdateSetRequestModel
from backend.src.routers.AuthorizationRouter import getCurrentActiveUser
from backend.src.services.cards.SetService import SetService

router = APIRouter(prefix="/set")


@router.post("/{setId}/bg")
async def upload(setId: str,
                 file: UploadFile,
                 user: Annotated[UserEntity, Depends(getCurrentActiveUser)],
                 session: Session = Depends(getDbSession)) -> Response:
    """
    Загрузка фонового изображения набора

    :param setId: id набора
    :param file: метаданные файла
    :param user: текущий авторизованный пользователь
    :param session: сессия соединения с БД
    :return: id загруженного файла
    """
    if not validateImage(file):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Загружаемый файл должен быть изображением размером не более 5 Мбайт")
    SetService(user, session).uploadBg(setId, file)
    return Response()


@router.get("/{setId}/bg")
async def getFile(setId: str,
                  user: Annotated[UserEntity, Depends(getCurrentActiveUser)],
                  session: Session = Depends(getDbSession)) -> Response:
    """
    Скачать фоновое изображение набора

    :param setId: id набора
    :param user: текущий авторизованный пользователь
    :param session: сессия соединения с БД
    :return: метаданные файла
    """
    return Response(SetService(user, session).downloadBg(setId), media_type="image/*")


@router.post("/create")
async def create(request: Annotated[UpdateSetRequestModel, Body()],
                 user: Annotated[UserEntity, Depends(getCurrentActiveUser)],
                 session: Session = Depends(getDbSession)) -> IdResponseModel:
    """
    Создать набор карточек

    :param request: тело запроса
    :param user: текущий авторизованный пользователь
    :param session: сессия соединения с БД
    :return: id созданного набора
    """
    return IdResponseModel(id=SetService(user, session).create(request))


@router.put("/{setId}")
async def update(setId: str,
                 request: Annotated[UpdateSetRequestModel, Body()],
                 user: Annotated[UserEntity, Depends(getCurrentActiveUser)],
                 session: Session = Depends(getDbSession)) -> IdResponseModel:
    """
    Обновить данные набора карточек

    :param setId: id набора
    :param request: тело запроса
    :param user: текущий авторизованный пользователь
    :param session: сессия соединения с БД
    :return: id созданного набора
    """
    return IdResponseModel(id=SetService(user, session).update(setId, request))
