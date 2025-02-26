import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, MagicMock
from sqlalchemy.orm import Session

from main import app
from src.transaction.schemas import TransactionUserInputSchema
from database import get_session  

client = TestClient(app)


from src.auth.utils import create_access_token  

@pytest.fixture
def mock_auth_user():
    return {"user_id": 1, "is_user": True}




@pytest.fixture
def mock_session():
    return Mock(spec=Session)

@pytest.fixture
def auth_header(mock_auth_user):
    """Generate a valid JWT token for authentication."""
    token = create_access_token(data=mock_auth_user)  # Generate a proper JWT token
    return {"Authorization": f"Bearer {token}"} # Simulated auth token

@pytest.fixture
def transaction_input():
    return {
        "vendor_name": "vendor1",
        "vendor_id": "2ec45e7a-8d6c-4bb7-9256-429975f556f9",
        "points": 50
    }

def test_user_vendor_transaction_success(mock_session, auth_header, transaction_input):
    app.dependency_overrides[get_session] = lambda: mock_session  

    # Mock vendor and user points
    mock_vendor = MagicMock()
    mock_vendor.id = 2
    mock_session.exec = Mock(side_effect=[
        MagicMock(first=Mock(return_value=mock_vendor)),  # Vendor exists
        MagicMock(first=Mock(return_value=100))  # User has enough points
    ])

    response = client.post(
        "/api/v1/transaction/user/vendor/transaction",
        json=transaction_input,
        headers=auth_header  # Use properly generated JWT token
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Points transfered successfully"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()

    

def test_user_vendor_transaction_no_vendor(mock_session, auth_header, transaction_input):
    app.dependency_overrides[get_session] = lambda: mock_session  

    # Mock vendor not found
    mock_session.exec = Mock(side_effect=[
        MagicMock(first=Mock(return_value=None))  # Vendor does not exist
    ])

    response = client.post(
        "/api/v1/transaction/user/vendor/transaction",
        json=transaction_input,
        headers=auth_header
    )

    assert response.status_code == 400
    assert response.json()["error"] == "No vendor details found"
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()


def test_user_vendor_transaction_no_points(mock_session, auth_header, transaction_input):
    app.dependency_overrides[get_session] = lambda: mock_session  

    # Mock vendor exists but user has no points
    mock_vendor = MagicMock()
    mock_vendor.id = 2
    mock_session.exec = Mock(side_effect=[
        MagicMock(first=Mock(return_value=mock_vendor)),  
        MagicMock(first=Mock(return_value=None))  # No points found
    ])

    response = client.post(
        "/api/v1/transaction/user/vendor/transaction",
        json=transaction_input,
        headers=auth_header
    )

    assert response.status_code == 400
    assert response.json()["error"] == "You don't have a points"
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()


def test_user_vendor_transaction_insufficient_points(mock_session, auth_header, transaction_input):
    app.dependency_overrides[get_session] = lambda: mock_session  

    # Mock vendor exists but user has insufficient points
    mock_vendor = MagicMock()
    mock_vendor.id = 2
    mock_session.exec = Mock(side_effect=[
        MagicMock(first=Mock(return_value=mock_vendor)),  
        MagicMock(first=Mock(return_value=30))  # User has fewer points than required
    ])

    response = client.post(
        "/api/v1/transaction/user/vendor/transaction",
        json=transaction_input,
        headers=auth_header
    )

    assert response.status_code == 400
    assert response.json()["error"] == "You don't have a enough points"
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()
