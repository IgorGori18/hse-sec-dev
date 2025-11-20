import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

if os.getenv("CI") == "true":
    DATABASE_URL = "sqlite:///:memory:"  # для CI
else:
    DATABASE_URL = "sqlite:///./studyplanner.db"  # контейнер

engine = create_engine(
    DATABASE_URL,
    connect_args=(
        {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
    ),
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
