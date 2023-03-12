from contextlib import contextmanager
from db.sql_pool import ConnectionPool, Connection

from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

PASSWORD_UPDATE = quote_plus(settings.MYSQL_ROOT_PASSWORD)
MYSQL_DATABASE_URI = f"mysql+pymysql://root:{PASSWORD_UPDATE}@{settings.MYSQL_SERVER}:{settings.MYSQL_PORT}/{settings.MYSQL_DB}"  # noqa
engine = create_engine(
    MYSQL_DATABASE_URI,
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,
    pool_pre_ping=True,
    echo=True,
    future=True,
    # connect_args={
    #     "keepalives": 1,
    #     "keepalives_idle": 30,
    #     "keepalives_interval": 10,
    #     "keepalives_count": 5,
    # }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)


def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()


@contextmanager
def connect_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()

# mysql_pool = ConnectionPool(name="mysql", pool_pre_ping=True, pool_recycle=3600)


# def get_db():
#     db = None
#     try:
#         db = mysql_pool.get_connection()
#         yield db
#     finally:
#         if db:
#             db.close()
#
#
# @contextmanager
# def connect_db():
#     db = None
#     try:
#         db = Connection()
#         yield db
#     finally:
#         if db:
#             db.close()
