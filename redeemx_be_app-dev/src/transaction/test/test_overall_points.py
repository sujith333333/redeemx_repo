from unittest.mock import patch, MagicMock
import pytest
from fastapi.testclient import TestClient

from src.auth.utils import create_access_token
from main import app

client = TestClient(app)

@pytest.fixture
def mock_auth_admin():
    return {"is_admin": True}

@pytest.fixture
def mock_auth_non_admin():
    return {"is_admin": False}

@pytest.fixture
def auth_header(mock_auth_admin):
    token = create_access_token(mock_auth_admin)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def non_auth_header(mock_auth_non_admin):
    token = create_access_token(mock_auth_non_admin)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def mock_session():
    mock_session = MagicMock()

    mock_result = MagicMock()
    mock_result.points_assigned_to_employee = 1000
    mock_result.points_assigned_to_employee_balance = 800
    mock_result.total_points_user_sends_to_vendor = 500
    mock_result.points_claimed_by_vendor = 300

    
    mock_session.exec.return_value.first.return_value = mock_result

    return mock_session

def test_get_overall_points_valid(mock_auth_admin, mock_session, auth_header):
    with patch("src.transaction.router.auth_user", mock_auth_admin), \
         patch("src.transaction.router.session", mock_session):
        
        print(f"Mocked session return value: {mock_session}")

        response = client.get("/api/v1/transaction/overallpoints",
                              params={"start_date": "2024-01-01", "end_date": "2024-01-31"},headers=auth_header )
        print(response.status_code)
        
        assert response.status_code == 200
        assert mock_auth_admin["is_admin"] is True
        data = response.json()["data"]
        print(data)
        assert data["points_assigned_to_employee"] == 0
        assert data["points_assigned_to_employee_balance"] == 0
        assert data["total_points_user_sends_to_vendor"] == 0
        assert data["points_claimed_by_vendor"] == 0
        assert data["points_yet_to_approve_to_vendor"] == 0

@patch("src.transaction.router.session")
@patch("src.transaction.router.auth_user")
def test_get_overall_points_unauthorized(mock_auth_non_admin, mock_session, non_auth_header):
    mock_auth_admin.return_value = {"is_admin": False}
    mock_session.return_value = mock_session()
    response = client.get(
        "/api/v1/transaction/overallpoints",
        headers=non_auth_header
    )
    assert response.status_code == 400
    assert response.json()["error"] == "You are not authorized"


@patch("src.transaction.router.session")
@patch("src.transaction.router.auth_user")
def test_get_overall_points_invalid_dates(mock_auth_admin, mock_session, auth_header):
    mock_auth_admin.return_value = {"is_admin": True}
    mock_session.return_value = mock_session()

    response = client.get(
        "/api/v1/transaction/overallpoints?start_date=2025-02-10&end_date=2025-01-10",
        headers=auth_header
    )

    print(response.json())

    assert response.status_code == 400
    assert response.json()["error"] == "Start date cannot be after end date."


@patch("src.transaction.router.session")
@patch("src.transaction.router.auth_user")
def test_get_monthly_points_valid(mock_auth_admin, mock_session,auth_header):
    mock_auth_admin.return_value = {"is_admin": True}
    mock_session.return_value = mock_session()

    response = client.get("/api/v1/transaction/monthlypoints?month=2&year=2025",headers=auth_header)

    print(f"Response Status Code: {response.status_code}")
    print(f"Response JSON: {response.json()}")

    assert response.status_code == 200, f"Unexpected response: {response.json()}"


@patch("src.transaction.router.auth_user", new_callable=lambda: mock_auth_non_admin)
def test_get_monthly_points_unauthorized(mock_auth_non_admin):
    response = client.get("/api/v1/transaction/monthlypoints?month=2&year=2025")
    assert response.status_code == 400
    assert response.json()["error"] == "You are not authorized"

@patch("src.transaction.router.session")
@patch("src.transaction.router.auth_user")
def test_get_monthly_points_unauthorized(mock_auth_non_admin, mock_session, non_auth_header):
    mock_auth_admin.return_value = {"is_admin": False}  
    mock_session.return_value = mock_session()  
    response = client.get(
        "/api/v1/transaction/monthlypoints?month=2&year=2025",
        headers=non_auth_header  
    )
    assert response.status_code == 400
    assert response.json()["error"] == "You are not authorized"

@patch("src.transaction.router.session")
@patch("src.transaction.router.auth_user")
def test_get_monthly_points_invalid_month(mock_auth_admin, mock_session,auth_header):
    response = client.get("/api/v1/transaction/monthlypoints?month=13&year=2025",headers=auth_header)
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid month. Must be between 1 and 12."

@patch("src.transaction.router.session")
@patch("src.transaction.router.auth_user")
def test_get_monthly_points_missing_year(mock_auth_admin, mock_session,auth_header):
    response = client.get("/api/v1/transaction/monthlypoints?month=2",headers=auth_header)
    assert response.status_code == 200
