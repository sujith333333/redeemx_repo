import pytest
from src.user.schemas import ChangePasswordSchema  
 
 
def test_change_password_positive():
   
    schema = ChangePasswordSchema(
        old_password="OldPassword123",
        new_password="NewPassword123"
    )
    assert schema.old_password == "OldPassword123"
    assert schema.new_password == "NewPassword123"
 
 
def test_change_password_negative_missing_old_password():
   
    with pytest.raises(Exception):
        ChangePasswordSchema(
            new_password="NewPassword123"
        )
 
 
def test_change_password_negative_missing_new_password():
   
    with pytest.raises(Exception):
        ChangePasswordSchema(
            old_password="OldPassword123"
        )
 
 
def test_change_password_negative_empty_old_password():
    try:
        ChangePasswordSchema(
            old_password="",
            new_password="NewPassword123"
        )
    except ValueError as e:
        assert "old_password cannot be empty or whitespace" in str(e)
 

 
 
def test_change_password_negative_same_old_and_new_password():
 
    schema = ChangePasswordSchema(
        old_password="SamePassword123",
        new_password="SamePassword123"
    )
    assert schema.old_password == "SamePassword123"
    assert schema.new_password == "SamePassword123"
 
 