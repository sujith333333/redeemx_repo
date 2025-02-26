import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app


from src.auth.utils import create_access_token

client = TestClient(app)


@pytest.fixture
def admin_user():
    return {"id": "user_id", "is_user": True}

@pytest.fixture
def auth_header(admin_user):
    token = create_access_token(admin_user)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_session():
    
    session = MagicMock()
    yield session


def test_user_with_points(auth_header, mock_session):
    mock_session.exec.return_value.first.return_value = (100,)
    response = client.get("/api/v1/transaction/user/points", headers=auth_header)

    assert response.status_code == 200
    assert response.json()["data"]["points"] == 10