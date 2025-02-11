from typing import Annotated

from fastapi import APIRouter, UploadFile, Depends, Body, HTTPException, status
from sqlalchemy.orm import Session
from starlette.responses import Response

from backend.src.Database import getDbSession
from backend.src.Utils import validateImage, getPaginated
from backend.src.entities.users.UserEntity import UserEntity
from backend.src.models.IdModel import IdModel
from backend.src.models.PaginatedResponse import PaginatedResponse
from backend.src.models.SetModel import BaseSetModel, FilterRequest, SetGradeRequestModel
from backend.src.routers.AuthorizationRouter import getCurrentActiveUser, getCurrentActiveUserOptional
from backend.src.services.SetService import SetService

router = APIRouter(prefix="/sets")


@router.post("/{setId}/bg")
async def uploadBg(setId: str,
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
async def downloadBg(setId: str,
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
async def create(request: Annotated[BaseSetModel, Body()],
                 user: Annotated[UserEntity, Depends(getCurrentActiveUser)],
                 session: Session = Depends(getDbSession)) -> IdModel:
    """
    Создать набор карточек

    :param request: тело запроса
    :param user: текущий авторизованный пользователь
    :param session: сессия соединения с БД
    :return: id созданного набора
    """
    return IdModel(id=SetService(user, session).create(request))


@router.put("/{setId}")
async def update(setId: str,
                 request: Annotated[BaseSetModel, Body()],
                 user: Annotated[UserEntity, Depends(getCurrentActiveUser)],
                 session: Session = Depends(getDbSession)) -> IdModel:
    """
    Обновить данные набора карточек

    :param setId: id набора
    :param request: тело запроса
    :param user: текущий авторизованный пользователь
    :param session: сессия соединения с БД
    :return: id обновленного набора
    """
    return IdModel(id=SetService(user, session).update(setId, request))


@router.post("/list")
async def getList(page: int,
                  size: int,
                  user: Annotated[UserEntity, Depends(getCurrentActiveUserOptional)],
                  filterData: Annotated[FilterRequest, Body()],
                  session: Session = Depends(getDbSession)) -> PaginatedResponse:
    """
    Запрос на получение табличного отображения наборов

    :param page: страница
    :param size: количество записей за раз
    :param filterData: данные фильтрации
    :param user: текущий авторизованный пользователь (если авторизован)
    :param session: сессия соединения с БД
    :return: список наборов
    """
    return getPaginated(page,
                        size,
                        SetService(user, session).getList(filterData),
                        lambda row: SetService.convertToTile(row[0]))


@router.post("/favorite")
async def getList(page: int,
                  size: int,
                  user: Annotated[UserEntity, Depends(getCurrentActiveUser)],
                  session: Session = Depends(getDbSession)):
    """
    Запрос на получение табличного отображения наборов

    :param page: страница
    :param size: количество записей за раз
    :param user: текущий авторизованный пользователь
    :param session: сессия соединения с БД
    :return: список наборов
    """
    return getPaginated(page,
                        size,
                        SetService(user, session).getFavoritesList(),
                        lambda row: SetService.convertToTile(row[-1]))


@router.get("/{setId}/favorite")
async def addSetToFavorites(setId: str,
                            user: Annotated[UserEntity, Depends(getCurrentActiveUser)],
                            session: Session = Depends(getDbSession)) -> Response:
    """
    Добавить набор в список избранного

    :param setId: id набора
    :param user: текущий авторизованный пользователь
    :param session: сессия соединения с БД
    :return: пустое тело ответа в случае отсутствия ошибок
    """
    SetService(user, session).addToFavorites(setId)
    return Response()


@router.post("/{setId}/grade")
async def addSetToFavorites(setId: str,
                            request: Annotated[SetGradeRequestModel, Body()],
                            user: Annotated[UserEntity, Depends(getCurrentActiveUser)],
                            session: Session = Depends(getDbSession)) -> Response:
    """
    Поставить набору оценку

    :param setId: id набора
    :param request: тело запроса
    :param user: текущий авторизованный пользователь
    :param session: сессия соединения с БД
    :return: пустое тело ответа в случае отсутствия ошибок
    """
    SetService(user, session).setGrade(setId, request.grade)
    return Response()
