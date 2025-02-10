from sqlalchemy import create_engine, Pool, Table
from sqlalchemy.event import listens_for
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseEntity = declarative_base()


@listens_for(engine, "connect")
def on_connect(dbapi_connection, connection_record):
    dbapi_connection.create_function("lower", 1, lambda s: s.lower())


def getDbSession() -> sessionmaker:
    """
    Получить сессию для БД
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
