from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

def check_name(name):
    """
        Check database name.
    """
    if not name:
        raise Exception("database name cannot be the empty string")

    invalid_chars = [" ", ".", "$", "/",'@']
    for invalid_char in invalid_chars:
        if invalid_char in name:
            raise Exception(f"database names cannot contain the character {invalid_char}")

check_name(settings.POSTGRES_DB)

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
