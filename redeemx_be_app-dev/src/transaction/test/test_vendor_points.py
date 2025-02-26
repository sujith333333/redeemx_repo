import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from main import app
from src.auth.utils import create_access_token

client = TestClient(app)


@pytest.fixture
def admin_vendor():
    return {"id": "vendor_id", "is_vendor": True}

@pytest.fixture
def auth_header(admin_vendor):
    token = create_access_token(admin_vendor)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def mock_session():
    
    session = MagicMock()
    yield session


def test_vendor_with_points(auth_header, mock_session):
   
    mock_session.exec.return_value.first.return_value = (100,)  

   
    response = client.get("/api/v1/transaction/vendor/points", headers=auth_header)

   
    assert response.status_code == 200
    print(response.json())
    assert "data" in response.json()
    assert "points" in response.json()["data"]  
    assert response.json()["data"]["points"] == {}  
