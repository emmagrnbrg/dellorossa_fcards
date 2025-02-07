from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from backend.src.exceptions.cards.SetNotFoundException import SetNotFoundException
from backend.src.models.db.cards.SetEntity import SetEntity
from backend.src.models.db.users.UserEntity import UserEntity
from backend.src.models.enum.AccessEnum import AccessEnum
from backend.src.models.enum.RightEnum import RightEnum
from backend.src.models.rest.cards.UpdateSetRequestModel import UpdateSetRequestModel


class SetService:
    """
    Сервис работы с наборами карточек
    """
    def __init__(self, currentUser: UserEntity, session: Session):
        self.__currentUser = currentUser
        self.__session = session

    def checkAccess(self, cardSet: SetEntity) -> bool:
        """
        Проверка доступа пользователя к набору

        :param cardSet: набор карточек
        :return: признак доступа пользователю карточек
        """
        if not self.__currentUser:
            return False

        canViewAllSets = RightEnum.VIEW_ALL_SETS in self.__currentUser.role.rights
        if canViewAllSets \
                or cardSet.owner.id == self.__currentUser.id \
                or cardSet.access in [AccessEnum.LINK_RESTRICTED, AccessEnum.PUBLIC]:
            return True

        if cardSet.access == AccessEnum.USER_RESTRICTED:
            return self.__currentUser.id in list(map(lambda member: member.id, cardSet.members))

        return False

    def create(self, request: UpdateSetRequestModel) -> int:
        """
        Создать набор карточек

        :param request: тело запроса
        :return: id созданного набора
        """
        if not self.__currentUser:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        setEntity: SetEntity = SetEntity(request.name, request.description, self.__currentUser)
        self.__session.add(setEntity)
        self.__session.commit()
        self.__session.refresh(setEntity)
        return setEntity.id

    def update(self, setId: str, request: UpdateSetRequestModel) -> int:
        """
        Обновить набор карточек

        :param setId: id редактируемого набора
        :param request: тело запроса
        :return: id созданного набора
        """
        if not self.__currentUser:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        setEntity: SetEntity = self.findById(setId)
        if not setEntity:
            raise SetNotFoundException()
        setEntity.name = request.name
        setEntity.description = request.description
        self.__session.add(setEntity)
        self.__session.commit()
        self.__session.refresh(setEntity)
        return setEntity.id

    def findById(self, setId: str) -> SetEntity | None:
        """
        Найти набор карточек по id

        :param setId: id набора
        :return: данные набора
        """
        return self.__session.query(SetEntity).filter(SetEntity.id == setId).first()

    def uploadBg(self, setId: str, file: UploadFile):
        """
        Загрузка фонового изображения набора

        :param setId: id набора
        :param file: метаданные файла
        :return: id загруженного файла
        """
        cardSet: SetEntity = self.findById(setId)
        if not cardSet or self.__currentUser.id != cardSet.owner.id:
            raise SetNotFoundException()

        cardSet.bg = file.file.read()

        self.__session.add(cardSet)
        self.__session.commit()
        self.__session.refresh(cardSet)

    def downloadBg(self, setId: str) -> bytes:
        """
        Получение фонового изображения набора

        :param setId: id набора
        :return: метаданные файла
        """
        cardSet: SetEntity = self.findById(setId)
        if not cardSet or not self.checkAccess(cardSet):
            raise SetNotFoundException()

        return cardSet.bg
