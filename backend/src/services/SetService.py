import datetime

from fastapi import UploadFile, HTTPException, status
from sqlalchemy import or_, and_, func, text
from sqlalchemy.orm import Session, Query

from backend.src.Constants import BASE_DATE_FORMAT
from backend.src.entities.sets.FavoriteSetEntity import FavoriteSetEntity
from backend.src.entities.sets.SetEntity import SetEntity
from backend.src.entities.sets.SetGradeEntity import SetGradeEntity
from backend.src.entities.sets.SetMemberEntity import SetMemberEntity
from backend.src.entities.users.UserEntity import UserEntity
from backend.src.enums.SetsEnum import AccessEnum, SetDateFilterEnum, SetSortEnum
from backend.src.enums.UsersEnum import RightEnum
from backend.src.exceptions.cards.SetNotFoundException import SetNotFoundException
from backend.src.models.SetModel import BaseSetModel, FilterRequest, TileSetResponse
from backend.src.models.UserModel import UserShortDataModel
from backend.src.services.users.UserService import UserService


class SetService:
    """
    Сервис работы с наборами карточек
    """

    def __init__(self, currentUser: UserEntity, session: Session):
        self.__currentUser = currentUser
        self.__session = session
        self.__userService = UserService(session)

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

    def create(self, request: BaseSetModel) -> int:
        """
        Создать набор карточек

        :param request: тело запроса
        :return: id созданного набора
        """
        if not self.__currentUser:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        members = list(filter(lambda user: user is not None,
                              map(lambda userId: self.__userService.findById(userId),
                                  request.userIds)))

        setEntity: SetEntity = SetEntity(request.name, request.description, self.__currentUser, members, request.access)
        self.__session.add(setEntity)
        self.__session.commit()
        self.__session.refresh(setEntity)
        return setEntity.id

    def update(self, setId: str, request: BaseSetModel) -> str:
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
        setEntity.access = request.access
        setEntity.modificationDate = datetime.date.today()

        if request.access == AccessEnum.USER_RESTRICTED:
            setEntity.members = list(filter(lambda user: user is not None,
                                            map(lambda userId: self.__userService.findById(userId),
                                                request.userIds)))
        else:
            setEntity.members = []

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
        cardSet.modificationDate = datetime.date.today()

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

    def getList(self, filterData: FilterRequest) -> Query:
        """
        Получить табличное отображение наборов

        :param filterData: данные фильтрации
        :return: список наборов (пагинированный)
        """
        query = self.__session.query(SetEntity, func.count(FavoriteSetEntity.c.set_id).label("favorites"))\
            .outerjoin(FavoriteSetEntity)\
            .group_by(SetEntity)

        # если пользователь не авторизован
        if not self.__currentUser:
            query = query.filter(SetEntity.access == AccessEnum.PUBLIC)
        else:
            # если нужно отображать наборы только текущего пользователя
            if filterData.mine:
                query = query.filter(SetEntity.ownerId == self.__currentUser.id)
            # если нет прав на просмотр всех наборов, отображаются созданные им + доступные ему
            elif not UserService.hasRight(self.__currentUser, RightEnum.VIEW_ALL_SETS):
                availableSetsIds = list(
                    map(
                        lambda row: row[0],
                        self.__session.query(SetMemberEntity.c.set_id) \
                            .filter(SetMemberEntity.c.member_id == self.__currentUser.id) \
                            .all()
                    )
                )
                query = query.filter(or_(
                    (SetEntity.access == AccessEnum.PUBLIC),
                    and_(SetEntity.ownerId == self.__currentUser.id),
                    and_(SetEntity.access == AccessEnum.USER_RESTRICTED, SetEntity.id.in_(availableSetsIds))
                ))

        if filterData.name:
            __name = filterData.name.lower()
            query = query.filter(SetEntity.name.ilike(f'%{__name}%'))

        if filterData.dateFilter and filterData.dateFilter != SetDateFilterEnum.ALL_TIME:
            query = query.filter(SetEntity.modificationDate >= filterData.dateFilter.getStartFrom())

        if filterData.sort == SetSortEnum.NEWEST_FIRST:
            query = query.order_by(SetEntity.modificationDate.desc())
        elif filterData.sort == SetSortEnum.BY_HIGHEST_GRADE:
            query = query.order_by(SetEntity.averageScore.desc())
        else:
            query = query.order_by(text('favorites DESC'))

        return query

    def getFavoritesList(self) -> Query:
        """
        Получить список наборов из избранного текущего авторизованного пользователя

        :return: список избранных наборов
        """
        return self.__session.query(FavoriteSetEntity, SetEntity)\
            .join(SetEntity, SetEntity.id == FavoriteSetEntity.c.set_id)\
            .filter(FavoriteSetEntity.c.user_id == self.__currentUser.id)

    def addToFavorites(self, setId: str) -> None:
        """
        Добавить набор в список избранного

        :param setId: id набора
        :return: пустое тело ответа в случае отсутствия ошибок
        """
        setEntity: SetEntity = self.findById(setId)
        if not setEntity or not self.checkAccess(setEntity):
            raise SetNotFoundException()
        setEntity.favorites.append(self.__currentUser)
        self.__session.commit()

    def setGrade(self, setId: str, grade: int) -> None:
        """
        Поставить набору оценку

        :param setId: id набора
        :param grade: оценка набору
        :return: пустое тело ответа в случае отсутствия ошибок
        """
        setEntity: SetEntity = self.findById(setId)
        if not setEntity or not self.checkAccess(setEntity):
            raise SetNotFoundException()

        setGrade = self.__session.query(SetGradeEntity).filter(and_(
            SetGradeEntity.setId == setId, SetGradeEntity.graderId == self.__currentUser.id
        )).first()
        if setGrade is None:
            setGrade = SetGradeEntity(setEntity, self.__currentUser)
        setGrade.grade = grade

        scoresAmount = len(setEntity.grades)
        # если оценок еще нет или набор оценен только текущим пользователем, просто меняем среднюю оценку на новую
        if scoresAmount == 0 or (scoresAmount == 1 and setGrade.id is not None):
            setEntity.averageScore = grade
        else:
            # если данный пользователь уже ставил оценку, вычтем ее из среднего значения
            # и затем пересчитаем его с новой оценкой
            if setGrade.id is not None:
                setEntity.averageScore = (setEntity.averageScore * scoresAmount - setGrade.grade) / (scoresAmount - 1)
            setEntity.averageScore = setEntity.averageScore + (grade - setEntity.averageScore) / (scoresAmount + 1)

        setEntity.averageScore = round(setEntity.averageScore, 2)
        self.__session.add(setGrade)
        self.__session.add(setEntity)

        self.__session.commit()

    @staticmethod
    def __calculateAvg(setEntity: SetEntity, newGrade: int = 0) -> float:
        """
        Рассчитать среднюю оценку для набора

        :param setEntity: набор карточек
        :param newGrade: новая оценка
        :return: средняя оценка набора
        """
        if not newGrade:
            return setEntity.averageScore

        gradesAmount = len(setEntity.grades)
        return setEntity.averageScore * (gradesAmount / (gradesAmount + 1)) + newGrade / (gradesAmount + 1)

    @staticmethod
    def convertToTile(entity: SetEntity) -> TileSetResponse:
        """
        Конвертировать набор карточек в модель для табличного отображения

        :param entity: сущность БД
        :return: модель для табличного отображения наборов
        """
        return TileSetResponse(
            id=entity.id,
            name=entity.name,
            author=UserShortDataModel(
                id=entity.owner.id,
                username=entity.owner.username
            ),
            description=entity.description,
            modificationDate=entity.modificationDate.strftime(BASE_DATE_FORMAT),
            cardsAmount=len(entity.cards),
            grade=entity.averageScore,
            favoritesCount=len(entity.favorites)
        )
