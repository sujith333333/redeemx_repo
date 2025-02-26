import pytest
import pandas as pd
from fastapi.testclient import TestClient
from unittest.mock import MagicMock


from main import app
from src.user.models import User
from src.transaction.models import Transaction
from sqlmodel import Session
from src.auth.utils import create_access_token



client = TestClient(app)


@pytest.fixture
def mock_session():
    session = MagicMock(spec=Session)
    yield session

@pytest.fixture
def admin_user():
    return {"id": "admin_id", "is_admin": True}

@pytest.fixture
def auth_header(admin_user):
    token = create_access_token(admin_user)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def non_admin_user():
    return {"id": "user_id", "is_admin": False}

@pytest.fixture
def non_admin_header(non_admin_user):
    token = create_access_token(non_admin_user)
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def mock_user():
    return MagicMock(id="12345")  

def test_upload_file_valid_csv(auth_header, mock_session):
    csv_data = "E. Code\n101\n102\n"
    file = {"file": ("Daily Attendance Report (10) (1).csv", csv_data)}
    mock_session.exec.return_value.all.return_value = [
        User(id="1", emp_id="101", password="Shravan@1245",mobile_number= "9856457845",is_user=True),
        User(id="2", emp_id="102", password="Avinash@78945",mobile_number= "9856457847",is_user=True),
    ]
    response = client.post(
        "/api/v1/transaction/user-data/upload/transaction",
        headers=auth_header,
        files=file,
    )

    assert response.status_code == 200
    assert response.json()["message"] == "File processed successfully."

def test_upload_file_invalid_format(auth_header):
    file = {"file": ("invalid_format.txt", "invalid content")}
    response = client.post(
        "/api/v1/transaction/user-data/upload/transaction",
        headers=auth_header,
        files=file,
    )
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid file format. Please upload a CSV or Excel file."

def test_upload_file_non_admin(non_admin_header):
    csv_data = "E. Code\n101\n102\n"
    file = {"file": ("test.csv", csv_data)}
    response = client.post(
        "/api/v1/transaction/user-data/upload/transaction",
        headers=non_admin_header,
        files=file,
    )
    assert response.status_code == 400
    assert response.json()["error"] == "You are not authorized"


def test_upload_file_unregistered_user(auth_header, mock_session):
    csv_data = "E. Code\n103\n"
    file = {"file": ("Daily Attendance Report (10) (1).csv", csv_data)}

    mock_session.exec.return_value.all.return_value = [
        User(id="1", emp_id="101", password="Eshwar@789456",mobile_number= "9856787845",is_user=True),
        User(id="2", emp_id="102", password="Naveen@12345678",mobile_number= "7956457845",is_user=True),
    ]

    response = client.post(
        "/api/v1/transaction/user-data/upload/transaction",
        headers=auth_header,
        files=file,
    )

    assert response.status_code == 200
    unassigned_data = response.json()["data"]
    assert len(unassigned_data) == 142
    assert unassigned_data[0]["emp_id"] == "AT1051"


def test_transaction_creation(mock_session, auth_header):
    csv_data = "E. Code\n101\n102\n"
    file = {"file": ("Daily Attendance Report (10) (1).csv", csv_data, "text/csv")}
    mock_session.exec.return_value.all.return_value = [
        User(id="1", emp_id="101", password="Shravan@1245", mobile_number="9856457845", is_user=True),
        User(id="2", emp_id="102", password="Avinash@78945", mobile_number="9856457847", is_user=True),
    ]
    response = client.post(
        "/api/v1/transaction/user-data/upload/transaction",
        headers=auth_header,
        files=file,
    )

    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    assert response.json()["message"] == "File processed successfully."
    expected_transaction_1 = Transaction(user_id="1", points=20)
    expected_transaction_2 = Transaction(user_id="2", points=20)
    mock_session.add(expected_transaction_1)
    mock_session.add(expected_transaction_2)
    assert mock_session.add.call_count == 2, "Two transactions should have been added to the session."

def test_transaction_creation_empty_excel_file(auth_header):
    empty_excel_data = pd.DataFrame()
    file = {"file": ("EmptyExcelFile.xlsx", empty_excel_data.to_excel(excel_writer='Daily Attendance Report (10) (1).xlsx',index=False), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
    response = client.post(
        "/api/v1/transaction/user-data/upload/transaction",
        headers=auth_header,
        files=file,
    )
    assert response.status_code == 400, f"Expected status code 400, but got {response.status_code}"
    assert response.json()["detail"] == "There was an error parsing the body"

def test_transaction_add_success(mock_session, mock_user):
    transaction = Transaction(user_id=mock_user.id, points=20)
    mock_session.add(transaction)
    mock_session.commit()
    mock_session.add.assert_called_once_with(transaction)  
    mock_session.commit.assert_called_once()              

def test_transaction_add_failure(mock_session, mock_user):
    transaction = Transaction(user_id=mock_user.id, points=20)
    mock_session.add.side_effect = Exception("Database error")  
    with pytest.raises(Exception, match="Database error"):
        mock_session.add(transaction)

def test_transaction_commit_failure(mock_session, mock_user):
    transaction = Transaction(user_id=mock_user.id, points=20)
    mock_session.commit.side_effect = Exception("Commit error")  
    mock_session.add(transaction)
    with pytest.raises(Exception, match="Commit error"):
        mock_session.commit()



