import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import Mock
from sqlmodel import select,func
from src.vendor.models import Vendor
from src.transaction.router import vendor_transaction_admin,user_get_points
from src.transaction.models import Transaction as TransactionSchema
from src.main import app

client = TestClient(app)

@pytest.fixture
def mock_session():
    session = Mock(spec=Session)
    session.exec = Mock()
    return session

@pytest.fixture
def auth_user_admin():
    return {"is_admin": True}

@pytest.fixture
def auth_user_non_admin():
    return {"is_admin": False}

@pytest.fixture
def transaction_data():
    return TransactionSchema(vendor_id=1, points=100)

def test_vendor_transaction_admin_success(mock_session, auth_user_admin, transaction_data):
    mock_vendor = Vendor(id=1,vendor_name='john123',email='john123@gmail.com',qr_code="qwertyuasdfghj")
    mock_session.exec.return_value.first.return_value = mock_vendor

    response = vendor_transaction_admin(
        transaction=transaction_data,
        response=Mock(),
        session=mock_session,
        auth_user=auth_user_admin
    )

    assert response.data == transaction_data
    assert response.message == "Points transfered successfully"
    mock_session.add.assert_called_once_with(transaction_data)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(transaction_data)

def test_vendor_transaction_admin_unauthorized(mock_session, auth_user_non_admin, transaction_data):
    response = vendor_transaction_admin(
        transaction=transaction_data,
        response=Mock(),
        session=mock_session,
        auth_user=auth_user_non_admin
    )

    assert response.error == "Your not authorized"
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()



