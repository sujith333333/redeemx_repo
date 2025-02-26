import pytest
from src.user.models import User
from src.vendor.models import Vendor


def test_user_positive():
    
    user = User(
        username="Rajesh12",
        name="Rajesh",
        password="StrongPass123",
        email="valid@gmail.com",
        mobile_number="9876543210",
    )
    assert user.username == "Rajesh12"
    assert user.name == "Rajesh"
    assert user.password == "StrongPass123"
    assert user.email == "valid@gmail.com"
    assert user.mobile_number == "9876543210"


def test_user_negative_invalid_username():
    with pytest.raises(Exception):
        user1 = User(
            username="R",
            name="Rajesh",
            password="StrongPass123",
            email="valid@gmail.com",
            mobile_number="9876543210",
        )

def test_user_negative_invalid_email():
    with pytest.raises(Exception):
        User(
            username="Rajesh12",
            name="Rajesh",
            password="StrongPass123",
            email="invalid-email",
            mobile_number="9876543210",
        )


def test_user_negative_weak_password():

    with pytest.raises(Exception):
        User(
            username="Rajesh12",
            name="Rajesh",
            password="weakpass", 
            email="valid@gmail.com",
            mobile_number="9876543210",
       
        )


def test_user_negative_invalid_mobile_number():

    with pytest.raises(Exception):
        User(
            username="Rajesh12",
            name="Rajesh",
            password="StrongPass123",
            email="valid@gmail.com",
            mobile_number="12345", 
          
        )
def test_user_negative_invalid_mobile_number2():

    with pytest.raises(Exception):
        User(
            username="Rajesh12",
            name="Rajesh",
            password="StrongPass123",
            email="valid@gmail.com",
            mobile_number="987654321s", 
          
        )


def test_user_negative_invalid_name():

    with pytest.raises(Exception):
        User(
            username="Rajesh12",
            name="Ra",
            password="StrongPass123",
            email="valid@gmail.com",
            mobile_number="9876543210",
        )


def test_user_negative_empty_fields():
    with pytest.raises(Exception):
        User(
            username="",
            name="Ra",
            password="StrongPass123",
            email="valid@gmail.com",
            mobile_number="9876543210",
          
           
        )