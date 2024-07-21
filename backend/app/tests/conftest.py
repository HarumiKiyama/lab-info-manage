from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, SQLModel
from app.crud import create_user
from app.core.config import settings
from app.core.db import engine, init_db
from app.main import app
from app.models import  User,UserCreate
from app.tests.utils.user import authentication_token_from_email
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        SQLModel.metadata.drop_all(engine)
    

@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def superuser_token_headers(client: TestClient, db:Session) -> dict[str, str]:
    user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            phonenum="17767193284",
            username=settings.FIRST_SUPERUSER,
            is_active=True,
        )
    create_user(session=db, user_create=user_in)
    return get_superuser_token_headers(client)


@pytest.fixture(scope="function")
def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
    user_in=UserCreate(
         email=settings.EMAIL_TEST_USER,
         password=settings.FIRST_SUPERUSER_PASSWORD,
         phonenum="boomboom",
         username=settings.EMAIL_TEST_USER,
    )
    create_user(session=db,user_create=user_in)
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db,
    )

@pytest.fixture(scope="function", autouse=True)
def cleanup_db(db:Session):
    yield
    statement = delete(User)
    db.exec(statement)
    db.commit()
