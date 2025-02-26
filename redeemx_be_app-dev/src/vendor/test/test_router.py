import pytest
from fastapi.testclient import TestClient
from src.main import app  
from src.auth.utils import create_access_token
from src.user.models import User
from src.database import get_session
from src.auth.schemas import UserLoginSchema
from unittest.mock import MagicMock
from datetime import datetime
from src.vendor.models import Vendor, Claim
from src.transaction.models import Transaction
from sqlmodel import select
from datetime import datetime,timezone

client = TestClient(app)
 
@pytest.fixture
def mock_db():
    db = MagicMock()
    return db
 
@pytest.fixture(autouse=True)
def override_dependency(mock_db):
    app.dependency_overrides[get_session] = lambda: mock_db
    yield
    app.dependency_overrides.clear()

vendor_data = {
        "name": "Arunaaaaaa",
        "username": "arunaaaaaaaa",
        "password": "ArunaAnnapurnaaaaaa1@",
        "emp_id": "AJA10008",
        "email": "arunaa02@gmail.com",
        "mobile_number": "9876543210",
        "is_vendor": 1,
        "vendor_name": "Arunaaaa",
        "description": "This is a test vendor"
    }
test_user = {
        "email": "admin@gmail.com", 
        "user_id": "1",  
        "is_admin": True,  
        "is_user": False,  
        "is_vendor": False, 
    }

test_user_1 = {
        "email": "admin@gmail.com", 
        "user_id": "1",  
        "is_admin": False,  
        "is_user": False,  
        "is_vendor": False, 
    }

test_user_2 = {
        "email": "admin@gmail.com", 
        "user_id": "1",  
        "is_admin": False,  
        "is_user": False,  
        "is_vendor": True, 
    }

test_vendor={
  "email": "aruna@gmail.com",
  "password": "AnnapurnaAruna@"
}

@pytest.fixture
def mock_db_existing_user(mock_db):
    mock_user = User(
        name="TestVendor",
        username="testvendor123",
        email="existing_vendor@example.com",
        password="TestPassword1@",
        emp_id="AJA12345",
        mobile_number="9876543210",
        is_vendor=True
    )
    mock_db.exec.return_value.first.return_value = mock_user

def create_test_token(data: dict):
    return create_access_token(data)

def test_vendor_registration(mock_db):
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = None
    response = client.post("/api/v1/vendor/register", json=vendor_data, headers=headers)
    assert response.status_code == 201

def test_vendor_registration_duplicate_email(mock_db_existing_user):
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    response_duplicate = client.post("/api/v1/vendor/register", json=vendor_data, headers=headers)
    print("Duplicate Registration Response:", response_duplicate.json()) 
    assert response_duplicate.status_code == 400

def test_vendor_registration_unauthorized():
    test_token = create_test_token(data=test_user_1)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.post("/api/v1/vendor/register", json=vendor_data, headers=headers)
    assert response.status_code == 401

def test_get_all_vendors_authorized():
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/vendor/get_all/vendors", headers=headers)
    assert response.status_code == 200

def test_get_all_vendors_unauthorized():
    test_token = create_test_token(data=test_user_1)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/vendor/get_all/vendors", headers=headers)
    assert response.status_code == 401

def test_get_vendor_details_authorized(mock_db):
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_vendor = MagicMock()
    mock_vendor.dict.return_value = {
        "vendor_name": "Test Vendor",
        "description": "This is a test vendor"
    }

    mock_user = MagicMock()
    mock_user.dict.return_value = {
        "email": "admin@gmail.com",
        "user_id": "1"
    }
    mock_db.exec.return_value.first.return_value = (mock_vendor, mock_user)
    response = client.get("/api/v1/vendor/get/vendors-details", headers=headers)
    assert response.status_code == 200

def test_get_vendor_details_not_found(mock_db):
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = None
    response = client.get("/api/v1/vendor/get/vendors-details", headers=headers)
    assert response.status_code == 400

def test_get_vendor_user_transactions_authorized(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"} 
    mock_db.exec.return_value.first.return_value = 1
    mock_db.exec.return_value.all.return_value = [
        MagicMock(user_id=3, points=50, created_at=datetime(2024, 1, 1))
    ]
    response = client.get("/api/v1/vendor/user/transactions", headers=headers)
    assert response.status_code == 200

def test_get_vendor_transactions_with_end_date_extension(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = 1
    mock_db.exec.return_value.all.return_value = [
        MagicMock(user_id=3, points=50, created_at=datetime(2024, 1, 31, 23, 59, 59)),  # Last second of the day
        MagicMock(user_id=4, points=20, created_at=datetime(2024, 2, 1, 0, 0, 1)),  # First second of next day
    ]

    response1 = client.get("/api/v1/vendor/user/transactions?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    response2 = client.get("/api/v1/vendor/admin/transactions?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    response3 = client.get("/api/v1/vendor/all/transactions?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    response4 = client.get("/api/v1/vendor/credited/points?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    response5 = client.get("/api/v1/vendor/debited/points?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    response6 = client.get("/api/v1/vendor/all/points?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200
    assert response4.status_code == 200
    assert response5.status_code == 200
    assert response6.status_code == 200

def test_get_vendor_user_transactions_by_month_year(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = 1
    mock_db.exec.return_value.all.return_value = [
        MagicMock(user_id=3, points=50, created_at=datetime(2024, 1, 15))
    ]
    response = client.get("/api/v1/vendor/user/transactions?month=1&year=2024", headers=headers)
    assert response.status_code == 200
    assert response.json()['data'][0]['points'] == -50 

    response = client.get("/api/v1/vendor/user/transactions?month=13&year=2024", headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == "Invalid month. Must be between 1 and 12."
    

    response = client.get("/api/v1/vendor/user/transactions?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.status_code == 200
    assert response.json()['data'][0]['points'] == -50

    response = client.get("/api/v1/vendor/user/transactions?start_date=2025-02-01&end_date=2024-01-31", headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == "Start date cannot be after end date."

    response = client.get("/api/v1/vendor/user/transactions?end_date=2024-01-31", headers=headers)
    assert response.status_code == 200

    response = client.get("/api/v1/vendor/user/transactions?start_date=2024-01-01", headers=headers)
    assert response.status_code == 200 

def test_get_vendor_user_transactions_vendor_not_found(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = None
    response = client.get("/api/v1/vendor/user/transactions?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.json()['error'] == "Vendor details not found"

def test_get_vendor_user_no_transactions_found(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.all.return_value = []
    response = client.get("/api/v1/vendor/user/transactions?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.json()['data'] ==[]
    assert response.json()["message"]=="No transactions found for the given criteria." 

def test_get_vendor_admin_transactions_authorized(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"} 
    mock_db.exec.return_value.first.return_value = 1
    mock_db.exec.return_value.all.return_value = [
        MagicMock(user_id=None, points=50, created_at=datetime(2024, 1, 1))
    ]
    response = client.get("/api/v1/vendor/admin/transactions", headers=headers)
    assert response.status_code == 200

def test_get_vendor_admin_transactions_by_month_year(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = 1
    mock_db.exec.return_value.all.return_value = [
        MagicMock(user_id=None, points=50, created_at=datetime(2024, 1, 15))
    ]
    response = client.get("/api/v1/vendor/admin/transactions?month=1&year=2024", headers=headers)
    assert response.status_code == 200
    assert response.json()['data'][0]['points'] == -50 

    response = client.get("/api/v1/vendor/admin/transactions?month=13&year=2024", headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == "Invalid month. Must be between 1 and 12."
    

    response = client.get("/api/v1/vendor/admin/transactions?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.status_code == 200
    assert response.json()['data'][0]['points'] == -50

    response = client.get("/api/v1/vendor/admin/transactions?start_date=2025-02-01&end_date=2024-01-31", headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == "Start date cannot be after end date."

    response = client.get("/api/v1/vendor/admin/transactions?end_date=2024-01-31", headers=headers)
    assert response.status_code == 200

    response = client.get("/api/v1/vendor/admin/transactions?start_date=2024-01-01", headers=headers)
    assert response.status_code == 200 

def test_get_vendor_admin_transactions_vendor_not_found(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = None
    response = client.get("/api/v1/vendor/admin/transactions?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.json()['error'] == "Vendor details not found"

def test_get_vendor_admin_no_transactions_found(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.all.return_value = []
    response = client.get("/api/v1/vendor/admin/transactions?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.json()['data'] ==[]
    assert response.json()["message"]=="No transactions found for the given criteria." 

def test_get_vendor_all_transactions_authorized(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"} 
    mock_db.exec.return_value.first.return_value = 1
    mock_db.exec.return_value.all.return_value = [
        MagicMock(user_id=None, points=50, created_at=datetime(2024, 1, 1))
    ]
    response = client.get("/api/v1/vendor/all/transactions", headers=headers)
    assert response.status_code == 200


def test_get_vendor_all_transactions_by_month_year(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = 1
    mock_db.exec.return_value.all.return_value = [
        MagicMock(user_id=None, points=50, created_at=datetime(2024, 1, 15))
    ]
    response = client.get("/api/v1/vendor/all/transactions?month=1&year=2024", headers=headers)
    assert response.status_code == 200
    assert response.json()['data'][0]['points'] == -50 

    response = client.get("/api/v1/vendor/all/transactions?month=13&year=2024", headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == "Invalid month. Must be between 1 and 12."
    

    response = client.get("/api/v1/vendor/all/transactions?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.status_code == 200
    assert response.json()['data'][0]['points'] == -50

    response = client.get("/api/v1/vendor/all/transactions?start_date=2025-02-01&end_date=2024-01-31", headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == "Start date cannot be after end date."

    response = client.get("/api/v1/vendor/all/transactions?end_date=2024-01-31", headers=headers)
    assert response.status_code == 200

    response = client.get("/api/v1/vendor/all/transactions?start_date=2024-01-01", headers=headers)
    assert response.status_code == 200 

def test_get_vendor_all_transactions_vendor_not_found(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = None
    response = client.get("/api/v1/vendor/all/transactions?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.json()['error'] == "Vendor details not found"

def test_get_vendor_all_no_transactions_found(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.all.return_value = []
    response = client.get("/api/v1/vendor/all/transactions?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.json()['data'] ==[]
    assert response.json()["message"]=="No transactions found for the given criteria." 

def test_get_vendor_credited_authorized(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"} 
    mock_db.exec.return_value.first.return_value = 1
    mock_db.exec.return_value.all.return_value = [
        MagicMock(user_id=3, points=50, created_at=datetime(2024, 1, 1))
    ]
    response = client.get("/api/v1/vendor/credited/points", headers=headers)
    assert response.status_code == 200

def test_get_vendor_credited_points_by_month_year(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = 1
    mock_db.exec.return_value.all.return_value = [
        MagicMock(user_id=3, points=50, created_at=datetime(2024, 1, 15))
    ]
    response = client.get("/api/v1/vendor/credited/points?month=1&year=2024", headers=headers)
    assert response.status_code == 200

    response = client.get("/api/v1/vendor/credited/points?month=13&year=2024", headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == "Invalid month. Must be between 1 and 12."
    
    response = client.get("/api/v1/vendor/credited/points?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.status_code == 200

    response = client.get("/api/v1/vendor/credited/points?start_date=2025-02-01&end_date=2024-01-31", headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == "Start date cannot be after end date."

    response = client.get("/api/v1/vendor/credited/points?day=2024-01-15", headers=headers)
    assert response.status_code == 200

def test_get_vendor_credited_points_vendor_not_found(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = None
    response = client.get("/api/v1/vendor/credited/points?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.json()['error'] == "Vendor details not found"

def test_get_vendor_debited_authorized(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"} 
    mock_db.exec.return_value.first.return_value = 1
    mock_db.exec.return_value.all.return_value = [
        MagicMock(user_id=None, points=50, created_at=datetime(2024, 1, 1))
    ]
    response = client.get("/api/v1/vendor/debited/points", headers=headers)
    assert response.status_code == 200


def test_get_vendor_debited_points_by_month_year(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = 1
    mock_db.exec.return_value.all.return_value = [
        MagicMock(user_id=None, points=50, created_at=datetime(2024, 1, 15))
    ]
    response = client.get("/api/v1/vendor/debited/points?month=1&year=2024", headers=headers)
    assert response.status_code == 200

    response = client.get("/api/v1/vendor/debited/points?month=13&year=2024", headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == "Invalid month. Must be between 1 and 12."
    
    response = client.get("/api/v1/vendor/debited/points?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.status_code == 200

    response = client.get("/api/v1/vendor/debited/points?start_date=2024-02-01&end_date=2024-01-31", headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == "Start date cannot be after end date."

    response = client.get("/api/v1/vendor/debited/points?day=2024-01-15", headers=headers)
    assert response.status_code == 200

def test_get_vendor_debited_points_vendor_not_found(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = None
    response = client.get("/api/v1/vendor/debited/points?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.json()['error'] == "Vendor details not found"

def test_get_vendor_all_points_authorized(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"} 
    mock_db.exec.return_value.first.return_value = 1
    mock_db.exec.return_value.all.return_value = [
        MagicMock(user_id=None, points=50, created_at=datetime(2024, 1, 1))
    ]
    response = client.get("/api/v1/vendor/all/points", headers=headers)
    assert response.status_code == 200


def test_get_vendor_all_points_by_month_year(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = 1
    mock_db.exec.return_value.all.return_value = [
        MagicMock(user_id=None, points=50, created_at=datetime(2024, 1, 15))
    ]
    response = client.get("/api/v1/vendor/all/points?month=1&year=2024", headers=headers)
    assert response.status_code == 200

    response = client.get("/api/v1/vendor/all/points?month=13&year=2024", headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == "Invalid month. Must be between 1 and 12."
    

    response = client.get("/api/v1/vendor/all/points?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.status_code == 200

    response = client.get("/api/v1/vendor/all/points?start_date=2024-02-01&end_date=2024-01-31", headers=headers)
    assert response.status_code == 400
    assert response.json()['error'] == "Start date cannot be after end date."

    response = client.get("/api/v1/vendor/all/points?day=2024-01-15", headers=headers)
    assert response.status_code == 200

def test_get_vendor_all_points_vendor_not_found(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = None
    response = client.get("/api/v1/vendor/all/points?start_date=2024-01-01&end_date=2024-01-31", headers=headers)
    assert response.json()['error'] == "Vendor details not found"

def test_create_claim_success(mock_db):
    test_token = create_test_token(data=test_user_2)  
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.side_effect = [
        Vendor(id=1, user_id="2", vendor_name="TestVendor", qr_code="valid_qr_code"), -2000,500]
    mock_db.add = MagicMock()
    mock_db.commit = MagicMock()
    mock_db.refresh = MagicMock()
    response = client.post("/api/v1/vendor/claim/request", json={"points": 500}, headers=headers)
    assert response.status_code == 201

def test_claim_request_not_vendor(mock_db):
    test_token = create_test_token(data=test_user_1)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.post("/api/v1/vendor/claim/request", json={"points": 500}, headers=headers)
    assert response.status_code == 403
    assert response.json()['error'] == "Only vendors can request claims"

def test_claim_request_vendor_not_found(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = None
    response = client.post("/api/v1/vendor/claim/request", json={"points": 100}, headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == "Vendor ID does not exist"

def test_claim_request_invalid_points(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.post("/api/v1/vendor/claim/request", json={"points": 0}, headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == "Points must be greater than 0."

def test_claim_request_exceeding_points(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.side_effect = [
        Vendor(id=1, user_id="2", vendor_name="TestVendor", qr_code="valid_qr_code"), 1000, 800,]
    response = client.post("/api/v1/vendor/claim/request", json={"points": 500}, headers=headers)
    assert response.status_code == 400
    assert "Maximum claimable points" in response.json()["error"]

def test_get_claims_requests_success(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_vendor_id = 1
    mock_claims = [
        Claim(id=1, vendor_id=mock_vendor_id, points=500, status="pending", created_at=datetime(2025, 2, 6)),
        Claim(id=2, vendor_id=mock_vendor_id, points=300, status="approved", created_at=datetime(2025, 2, 5)),
    ]  
    mock_db.exec.side_effect = [
        MagicMock(first=MagicMock(return_value=mock_vendor_id)),  
        MagicMock(all=MagicMock(return_value=mock_claims)) 
    ]
    response = client.get("/api/v1/vendor/claim/requests", headers=headers)
    assert response.status_code == 200

def test_get_claims_vendor_not_found(mock_db):
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.side_effect = [MagicMock(first=MagicMock(return_value=None))]
    response = client.get("/api/v1/vendor/claim/requests", headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == "Vendor details not found."

def test_get_claims_vendor_not_authenticated(mock_db):
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.side_effect = [MagicMock(first=MagicMock(return_value=None))]
    response = client.get("/api/v1/vendor/claim/requests", headers=headers)
    assert response.status_code == 403
    assert response.json()["error"] == "Only vendors can request claims."

def test_get_claims_requests_filtered_by_status(mock_db):    
    test_token = create_test_token(data=test_user_2)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.side_effect = [1]  # Vendor ID exists
    mock_claims = [
        Claim(id=1, vendor_id=1, points=500, status="Pending", created_at=datetime(2024, 1, 10)),
        Claim(id=2, vendor_id=1, points=300, status="Pending", created_at=datetime(2024, 1, 8)),
    ]
    mock_db.exec.return_value.all.return_value = mock_claims  # Mocking .all() for status filter
    response = client.get("/api/v1/vendor/claim/requests?status=Pending", headers=headers)
    assert response.status_code == 200

def test_approve_claim_success(mock_db):    
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_claim = MagicMock()
    mock_claim.id = "1"
    mock_claim.points = 200 
    mock_claim.vendor_id = "vendor_123"

    mock_vendor = MagicMock()
    mock_vendor.id = "vendor_123"
    mock_db.exec.return_value.first.side_effect = [mock_claim, mock_vendor]
    response = client.put("/api/v1/vendor/admin/approve/1", json={"approved_points": 100}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Claim approved successfully with 100 points"

def test_approve_claim_not_admin():    
    test_token = create_test_token(data=test_user_1)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.put("/api/v1/vendor/admin/approve/1", json={"approved_points": 400}, headers=headers)
    assert response.status_code == 401
    assert response.json()["error"] == "You are not authorized to approve claims"

def test_approve_claim_not_found(mock_db):    
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec().first.side_effect = [None] 
    response = client.put("/api/v1/vendor/admin/approve/999", json={"approved_points": 400}, headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == "Claim not found"

def test_approve_claim_vendor_not_found(mock_db):    
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_claim = Claim(id=1, vendor_id=1, points=500, status="Pending", updated_at=datetime.utcnow())
    mock_db.exec.return_value.first.side_effect = [mock_claim, None]  
    response = client.put("/api/v1/vendor/admin/approve/1", json={"approved_points": 400}, headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == "Vendor does not exist"

def test_approve_claim_invalid_points(mock_db):
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_claim = Claim(id=1, vendor_id=1, points=500, status="Pending", updated_at=datetime.utcnow())
    mock_vendor = Vendor(id=1, user_id="2", vendor_name="TestVendor")
    mock_db.exec.return_value.first.side_effect = [mock_claim, mock_vendor]
    response = client.put("/api/v1/vendor/admin/approve/1", json={"approved_points": 600}, headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == "Approved points must be between 1 and the requested amount"

def test_reject_claim_success(mock_db):    
    test_token = create_test_token(data=test_user)  
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_claim = MagicMock()
    mock_claim.id = "1"
    mock_claim.status = "PENDING" 
    mock_claim.updated_at = None
    mock_db.exec.return_value.first.return_value = mock_claim
    response = client.put("/api/v1/vendor/admin/reject/1", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Claim rejected successfully"
    assert mock_claim.status == "REJECTED"  
    assert mock_claim.updated_at is not None  

def test_reject_claim_unauthorized(mock_db):    
    test_token = create_test_token(data=test_user_1)  
    headers = {"Authorization": f"Bearer {test_token}"}
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.put("/api/v1/vendor/admin/reject/1", headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == "You are not authorized to reject claims"

def test_reject_claim_not_found(mock_db):    
    test_token = create_test_token(data=test_user) 
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = None
    response = client.put("/api/v1/vendor/admin/reject/1", headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == "Claim not found"

def test_get_all_claims_admin_unauthorized(mock_db):
    test_token = create_test_token(data=test_user_1) 
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/vendor/claims/by/admin", headers=headers)
    assert response.status_code == 403
    assert response.json()["error"] == "Only admin can see the claim requests"

def test_get_all_claims_admin_success_no_filters(mock_db):
    test_token = create_test_token(data=test_user) 
    headers = {"Authorization": f"Bearer {test_token}"}
    fake_claim = Claim(
        id=1,
        vendor_id=2,
        points=500,
        status="APPROVED",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    fake_vendor_name = "VendorA"
    mock_db.exec.return_value.all.return_value = [(fake_claim, fake_vendor_name)]
    response = client.get("/api/v1/vendor/claims/by/admin", headers=headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)
    assert len(data) == 1
    claim_data = data[0]
    assert claim_data["id"] == str(fake_claim.id)
    assert claim_data["vendor_id"] == str(fake_claim.vendor_id)
    assert claim_data["vendor_name"] == fake_vendor_name
    assert claim_data["points"] == fake_claim.points
    assert claim_data["status"] == fake_claim.status
    assert "created_at" in claim_data
    assert "updated_at" in claim_data

def test_get_all_claims_admin_with_filters(mock_db):
    test_token = create_test_token(data=test_user) 
    headers = {"Authorization": f"Bearer {test_token}"}
    fake_claim = Claim(
        id=2,
        vendor_id=3,
        points=250,
        status="PENDING",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    fake_vendor_name = "VendorB"
    mock_db.exec.return_value.all.return_value = [(fake_claim, fake_vendor_name)]
    response = client.get("/api/v1/vendor/claims/by/admin?status=PENDING&vendor_name=VendorB", headers=headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 1
    claim_data = data[0]
    assert claim_data["id"] == str(fake_claim.id)
    assert claim_data["vendor_id"] == str(fake_claim.vendor_id)
    assert claim_data["vendor_name"] == fake_vendor_name
    assert claim_data["points"] == fake_claim.points
    assert claim_data["status"] == fake_claim.status

def test_get_vendor_remaining_points_unauthorized(mock_db):
    test_token = create_test_token(data=test_user) 
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/vendor/claim/points", headers=headers)
    assert response.status_code == 403
    assert response.json()["error"] == "Only vendors can get requested claims."

def test_get_vendor_remaining_points_vendor_not_found(mock_db):
    test_token = create_test_token(data=test_user_2) 
    headers = {"Authorization": f"Bearer {test_token}"}
    mock_db.exec.return_value.first.return_value = None
    response = client.get("/api/v1/vendor/claim/points", headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == "Vendor ID does not exist"

def test_get_vendor_remaining_points_success(mock_db):
    test_token = create_test_token(data=test_user_2) 
    headers = {"Authorization": f"Bearer {test_token}"}
    fake_vendor = MagicMock(spec=Vendor)
    fake_vendor.id = "vendor_1"
    fake_vendor.vendor_name = "TestVendor"
    mock_db.exec.return_value.first.side_effect = [fake_vendor, -100, 20]
    response = client.get("/api/v1/vendor/claim/points", headers=headers)
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["vendor_id"] == fake_vendor.id
    assert data["vendor_name"] == fake_vendor.vendor_name
    assert data["total_points"] == 100
    assert data["pending_points"] == 20
    assert data["usable_points"] == 80

