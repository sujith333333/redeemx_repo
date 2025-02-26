import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import MagicMock
from sqlmodel import Session
from src.database import get_session
from src.auth.utils import create_access_token
from fastapi import Request

client = TestClient(app)


@pytest.fixture
def mock_session():
    session = MagicMock(spec=Session)
    yield session

@pytest.fixture
def valid_transaction():
    return {"points": 255, "user_id":"4a494345-0d1e-4e4a-921e-9eb58ff9a405"}  

@pytest.fixture
def mock_admin_user():
    return {"is_admin": True}

@pytest.fixture
def mock_non_admin_user():
    return {"is_admin": False}

@pytest.fixture
def auth_header(mock_admin_user):
    token = create_access_token(mock_admin_user)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def non_admin_header(mock_non_admin_user):
    token = create_access_token(mock_non_admin_user)
    return {"Authorization": f"Bearer {token}"}



def test_admin_transaction_success(valid_transaction,auth_header,mock_session):
    app.dependency_overrides[get_session] = lambda: mock_session
    response = client.post(
        "/api/v1/transaction/admin/user/transaction",
        json=valid_transaction,
        headers=auth_header)
    
    assert response.status_code == 201
    assert response.json()["message"] == "Points added successfully"


def test_non_admin_transaction(non_admin_header, valid_transaction):
    response = client.post(
        "/api/v1/transaction/admin/user/transaction",
        json=valid_transaction,
        headers=non_admin_header
    )
    assert response.status_code == 200
    assert response.json()["error"] == "Your not authorized"



