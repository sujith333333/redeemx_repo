import pytest
from fastapi.testclient import TestClient
from fastapi import UploadFile
from unittest.mock import Mock, patch
import io
from main import app  
from database import get_session
import os

client = TestClient(app)

@pytest.fixture
def mock_session():
    session = Mock()
    session.add = Mock()
    session.commit = Mock()
    return session

@pytest.fixture(autouse=True)
def override_dependency(mock_session):
    app.dependency_overrides[get_session] = lambda: mock_session
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def valid_csv_file():
    csv_content = (
        "Emp ID,Name,Official Mobile Number,Email\n"
        "123,John Doeaa,9876543210,johndoaae@example.com\n"
        "456,Jane Doeaa,8765432109,janedoaae@example.com\n"
    )
    file = Mock(spec=UploadFile)
    file.filename = "test.csv"
    file.file = io.BytesIO(csv_content.encode("utf-8"))
    file.content_type = "text/csv"
    file.seek = Mock()  
    return file

@pytest.fixture
def csv_with_missing_fields():
    content = """Emp ID,Name,Official Mobile Number,Email
101,,1234567890,john.doea@example.com
,Jane Doe,,jane.doea@example.com"""
    file = UploadFile(filename="test.csv", file=io.BytesIO(content.encode()))
    return file

@pytest.fixture
def invalid_csv_file():
    return UploadFile(filename="test.txt", file=io.BytesIO(b"Invalid content"))

@pytest.fixture
def empty_csv_file():
    file = UploadFile(filename="test.csv", file=io.BytesIO(b""))
    return file

def test_upload_valid_csv(valid_csv_file, mock_session):
    with patch("src.utils.generate_password", return_value="Password123"):
        response = client.post(
            "/api/v1/user-upload/user/data/upload-excel/",
            files={"file": ("test.csv", valid_csv_file.file, "text/csv")},
        ) 
    assert response.status_code == 200
    assert response.json() == {"message": "Excel data successfully loaded into the database."}

def test_upload_invalid_file(invalid_csv_file):
    response = client.post(
        "/api/v1/user-upload/user/data/upload-excel/",
        files={"file": ("test.txt", invalid_csv_file.file, "text/plain")},
    )
    assert response.status_code == 400

def test_logger():
    logger_path = "logs/error.log"
    with open(logger_path, "w") as log_file:
        log_file.write("Test log entry")
    
    assert os.path.exists(logger_path)
    with open(logger_path, "r") as log_file:
        log_content = log_file.read()
    
    assert "Test log entry" in log_content
