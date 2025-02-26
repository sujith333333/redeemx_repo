import pytest
from fastapi.testclient import TestClient
from src.main import app  
from src.auth.utils import create_access_token
from src.user.models import User
from src.database import get_session
from src.auth.schemas import UserLoginSchema
from unittest.mock import MagicMock
from datetime import datetime,timedelta
from src.transaction.models import Transaction
import uuid
from src.user.utils import hash_password

from datetime import datetime
from src.transaction.models import Transaction
import uuid
from src.user.utils import hash_password
import unittest
from unittest.mock import patch, MagicMock
import io
import pandas as pd
import calendar



client = TestClient(app)
 
@pytest.fixture
def mock_db():
    db = MagicMock()
    db.exec().first.return_value = None
    return db
  
 
@pytest.fixture(autouse=True)
def override_dependency(mock_db):
    app.dependency_overrides[get_session] = lambda: mock_db
    yield
    app.dependency_overrides.clear()

user_data = {
        "username": "JohnnDoe",
        "name": "Johnn",
        "password": "SecurePass123",
        "email": "johnn@example.com",
        "mobile_number": "9876543219"
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
 
 
def create_test_token(data: dict):
    return create_access_token(data)

  
def test_register_positive(mock_db):
    mock_db.exec().first.return_value = None
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.post("/api/v1/user/register", json=user_data, headers=headers)
    assert response.status_code == 201


def test_register_positive1(mock_db):
    mock_user = User(
        username="JohnDoe",
        name="John",
        password="SecurePass123",
        email="john@example.com",
        mobile_number="9876543210",
        is_admin=False,
        is_user=True
    )
    mock_db.exec().first.return_value = mock_user
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.post("/api/v1/user/register", json=user_data, headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == f"{mock_user.email} is already exists"
 

def test_register_negitive(mock_db):
    mock_db.exec().first.return_value = None
    test_token = create_test_token(data=test_user_1)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.post("/api/v1/user/register", json=user_data, headers=headers)
    assert response.status_code == 401

    
def test_get_all_users_positive(mock_db):
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/user/get_all/users", headers=headers)
    assert response.status_code == 200

    
def test_get_all_users_negitive(mock_db):
    test_token = create_test_token(data=test_user_1)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/user/get_all/users", headers=headers)
    assert response.status_code == 401



def test_get_credit_transactions(mock_db):
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/user/credit-transactions", headers=headers)
    assert response.status_code == 200
    

def test_invalid_end_date_credit():
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/user/credit-transactions?start_date=2024-03-30&end_date=2024-02-26",headers=headers)
    assert response.status_code == 400
    

def test_get_debit_transactions(mock_db):
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/user/debit-transactions", headers=headers)    
    assert response.status_code == 200
    

def test_invalid_end_date_debit(mock_db):
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/user/debit-transactions?start_date=2024-03-30&end_date=2024-02-26", headers=headers)    
    assert response.status_code == 400
    

def test_get_recent_transactions(mock_db):
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/user/recent-transactions", headers=headers)
    assert response.status_code == 200
    

def test_invalid_end_date(mock_db):
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/user/recent-transactions?start_date=2024-03-30&end_date=2024-02-26", headers=headers)
    assert response.status_code == 400
    

def test_change_password_success(mock_db):
    user_id = str(uuid.uuid4())  
    hashed_password = hash_password("Password123")  
    mock_user = User(id=user_id, password=hashed_password, mobile_number="9234567890")
    mock_db.get.return_value = mock_user
    test_token = create_test_token(data={"user_id": user_id})
    headers = {"Authorization": f"Bearer {test_token}"}
    data = {"old_password": "Password123", "new_password": "Password123456"}
    response = client.patch("/api/v1/user/change-password", json=data, headers=headers)
    assert response.status_code == 200
    
   
def test_change_password_failure(mock_db):
    user_id = str(uuid.uuid4())  
    hashed_password = hash_password("Password123")  
    mock_user = User(id=user_id, password=hashed_password, mobile_number="9234567890")
    mock_db.get.return_value = mock_user
    test_token = create_test_token(data={"user_id": user_id})  
    headers = {"Authorization": f"Bearer {test_token}"}
    data = {"old_password": "Password12", "new_password": "Password123456"}
    response = client.patch("/api/v1/user/change-password", json=data, headers=headers)
    assert response.status_code == 400

 
def test_change_password_success(mock_db):
    user_id = str(uuid.uuid4())  
    hashed_password = hash_password("Password123")  
    mock_user = User(id=user_id, password=hashed_password, mobile_number="9234567890")
    mock_db.get.return_value = mock_user
    test_token = create_test_token(data={"user_id": user_id}) 
    headers = {"Authorization": f"Bearer {test_token}"}
    data = {"old_password": "Password123", "new_password": "Password123456"}
    response = client.patch("/api/v1/user/change-password", json=data, headers=headers)
    assert response.status_code == 200
    
    
def test_change_password_failure(mock_db):
    user_id = str(uuid.uuid4())  
    hashed_password = hash_password("Password123")  
    mock_user = User(id=user_id, password=hashed_password, mobile_number="9234567890")
    mock_db.get.return_value = mock_user
    test_token = create_test_token(data={"user_id": user_id})  
    headers = {"Authorization": f"Bearer {test_token}"}
    data = {"old_password": "Password12", "new_password": "Password123456"} 
    response = client.patch("/api/v1/user/change-password", json=data, headers=headers)
    assert response.status_code == 400


test_user2 = {
    "email": "user@gmail.com",
    "user_id": "1",
    "is_admin": False,
    "is_user": True,
    "is_vendor": False,
}

test_user_invalid3 = {
    "email": "user@gmail.com",
    "user_id": "1",
    "is_admin": False,
    "is_user": False,
    "is_vendor": False,
}


def get_month_range(year: int, month: int):
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
    return first_day, last_day

def test_all_points_no_dates(mock_db):
    test_token = create_test_token(data=test_user2)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/user/all/points/", headers=headers)
    assert response.status_code == 200


def test_all_points_invalid_month(mock_db):
    test_token = create_test_token(data=test_user2)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/user/all/points/?month=13&year=2024", headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid month. Must be between 1 and 12."


def test_all_points_missing_dates(mock_db):
    test_token = create_test_token(data=test_user2)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/user/all/points/?start_date=2024-01-01", headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == "Both start_date and end_date must be provided together."


def test_all_points_start_after_end(mock_db):
    test_token = create_test_token(data=test_user2)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/user/all/points/?start_date=2024-01-10&end_date=2024-01-01", headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == "Start date cannot be after end date."

def test_all_points_user_not_found(mock_db):
    mock_db.exec().first.return_value = None 
    test_token = create_test_token(data=test_user2)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/user/all/points/", headers=headers)
    assert response.status_code == 200  
    assert response.json()["error"] == "User details not found"


def test_all_points_success(mock_db):
    mock_db.exec().first.side_effect = [1, 500, 300, 200]
    test_token = create_test_token(data=test_user2)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.get("/api/v1/user/all/points/", headers=headers)
    assert response.status_code == 200
    assert response.json()["data"] == [{
        "balance": 500,
        "credited": 300,
        "debited": 200
    }]


def test_all_points_start_end(mock_db):
    test_token = create_test_token(data=test_user2)
    headers = {"Authorization": f"Bearer {test_token}"}
    start_date, end_date = get_month_range(2024, 1)
    response = client.get(f"/api/v1/user/all/points/?start_date=2025-01-09&end_date=2025-01-30", headers=headers)
    assert response.status_code == 200


def test_delete_user_success(mock_db):
    user_id = str(uuid.uuid4())
    mock_user = MagicMock()
    mock_user.id = user_id
    mock_user.email = "test@example.com"
    mock_user.password = "SecurePass123"
    mock_db.exec().first.return_value = mock_user
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.delete(f"/api/v1/user/delete-user/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json().get("message") == "User deleted successfully"

def test_delete_user_not_found(mock_db):
    user_id = str(uuid.uuid4())
    mock_db.exec().first.return_value = None
    test_token = create_test_token(data=test_user)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.delete(f"/api/v1/user/delete-user/{user_id}", headers=headers)
    assert response.status_code == 400
    assert response.json()["error"] == "User not found"

def test_delete_user_unauthorized(mock_db):
    user_id = str(uuid.uuid4())
    test_token = create_test_token(data=test_user_1)
    headers = {"Authorization": f"Bearer {test_token}"}
    response = client.delete(f"/api/v1/user/delete-user/{user_id}", headers=headers)
    assert response.status_code == 401
    assert response.json().get("error") == "You are not authorized"


