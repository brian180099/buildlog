import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import create_db_engine, get_db
from app.main import app
from app.models import Base


@pytest.fixture
def client():
    engine = create_db_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    def override_get_db():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = get_current_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(engine)


def test_register_me_and_logout_flow(client: TestClient) -> None:
    register = client.post(
        "/api/auth/register",
        json={
            "email": "learner@example.com",
            "password": "correct-horse-battery",
            "nickname": "학습자",
        },
    )

    assert register.status_code == 201
    assert register.json()["data"]["nickname"] == "학습자"
    assert "buildlog_session" in register.cookies

    me = client.get("/api/auth/me")
    assert me.status_code == 200
    assert me.json()["data"]["email"] == "learner@example.com"

    logout = client.post("/api/auth/logout")
    assert logout.status_code == 200
    assert client.get("/api/auth/me").status_code == 401


def test_duplicate_email_or_nickname_is_rejected(client: TestClient) -> None:
    payload = {
        "email": "learner@example.com",
        "password": "correct-horse-battery",
        "nickname": "learner",
    }
    assert client.post("/api/auth/register", json=payload).status_code == 201

    duplicate = client.post(
        "/api/auth/register",
        json={**payload, "nickname": "another"},
    )
    assert duplicate.status_code == 409


def test_invalid_login_does_not_create_a_session(client: TestClient) -> None:
    client.post(
        "/api/auth/register",
        json={
            "email": "learner@example.com",
            "password": "correct-horse-battery",
            "nickname": "learner",
        },
    )
    client.post("/api/auth/logout")

    response = client.post(
        "/api/auth/login",
        json={"email": "learner@example.com", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert client.get("/api/auth/me").status_code == 401


def test_user_can_change_their_nickname(client: TestClient) -> None:
    client.post(
        "/api/auth/register",
        json={
            "email": "learner@example.com",
            "password": "correct-horse-battery",
            "nickname": "learner",
        },
    )

    response = client.patch("/api/auth/me", json={"nickname": "새학습자"})

    assert response.status_code == 200
    assert response.json()["data"]["nickname"] == "새학습자"
