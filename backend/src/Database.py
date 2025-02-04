from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseEntity = declarative_base()


def getDbSession() -> sessionmaker:
    """
    Получить сессию для БД
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class RepresentativeModel:
    """
    Модель для вывода данных сущностей в удобочитаемом виде
    """
    def __repr__(self):
        fields = [f"{item[0]}={str(item[1])}" for item in self.__dict__.items() if item[0] != '_sa_instance_state']
        return f"{self.__class__.__name__}({', '.join(fields)})"
