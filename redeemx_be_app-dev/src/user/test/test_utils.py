import pytest
from passlib.context import CryptContext
from src.user.utils import hash_password, verify_password, generate_password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def test_hash_password_positive():
    password = "StrongPass123"
    hashed_password = hash_password(password)
    assert pwd_context.verify(password, hashed_password)

def test_hash_password_negative():
    password = "StrongPass123"
    wrong_password = "WrongPass456"
    hashed_password = hash_password(password)
    assert not pwd_context.verify(wrong_password, hashed_password)

def test_verify_password_positive():
    plain_password = "ValidPassword123"
    hashed_password = hash_password(plain_password)
    assert verify_password(plain_password, hashed_password)

def test_verify_password_negative():
    plain_password = "ValidPassword123"
    wrong_password = "InvalidPassword456"
    hashed_password = hash_password(plain_password)
    assert not verify_password(wrong_password, hashed_password)  

def test_generate_password_positive():
    name = "Rajesh"
    emp_id = "1234"
    password = name + "@" + emp_id
    hashed_password = generate_password(name, emp_id)
    assert pwd_context.verify(password, hashed_password)
def test_generate_password_negative_mismatch():
    name = "Rajesh"
    emp_id = "1234"
    wrong_name = "Ramesh"
    password = name + "@" + emp_id
    wrong_password = wrong_name + "@" + emp_id
    hashed_password = generate_password(name, emp_id)
    assert not pwd_context.verify(wrong_password, hashed_password)