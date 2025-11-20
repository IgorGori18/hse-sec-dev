import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base, get_db
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    os.environ["CI"] = "true"

    TEST_DB_PATH = "tests/test.db"
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    TEST_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


@pytest.fixture(autouse=True)
def clear_tokens():
    from app.auth import TOKENS

    TOKENS.clear()


@pytest.fixture()
def client():
    return TestClient(app)
