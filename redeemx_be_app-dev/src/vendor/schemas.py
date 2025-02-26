from sqlmodel import SQLModel, Field
from pydantic import EmailStr, validator
from datetime import datetime
import re

class VendorInputSchema(SQLModel):
    name: str = Field(..., min_length=2, max_length=100, description="Name must be between 2 and 100 characters.")
    username: str = Field(..., min_length=3, max_length=50, regex="^[a-zA-Z0-9_]+$", description="Username must be alphanumeric and at least 3 characters long.")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long and contain uppercase, lowercase, digit, and special character.")
    emp_id: str | None = Field(None, regex="^[a-zA-Z0-9]+$", description="Employee ID must be alphanumeric.")
    email: EmailStr = Field(..., description="Must be a valid email address.")
    mobile_number: str = Field(..., min_length=10, max_length=10, regex="^[0-9]{10}$", description="Mobile number must be exactly 10 digits.")
    vendor_name: str = Field(..., min_length=2, max_length=100, description="Vendor name must be between 2 and 100 characters.")
    description: str | None = Field(None, max_length=500, description="Description must not exceed 500 characters.")

    bank_name:str=Field(...,min_length=3,max_length=100, description="Bank name must be between 3 and 100 characters.")
    account_holder_name:str=Field(...,min_length=3,max_length=100, description="Account holder name must be between 3 and 100 characters.")
    account_number:str=Field(...,min_length=8,max_length=20,regex="^\d{8,20}$",description="Account number must be between 8 and 20 digits.")
    ifsc_code:str=Field(...,min_length=11,max_length=11,regex="^[A-Z]{4}0[A-Z0-9]{6}$",description="IFSC code must be valid.")
    branch_name:str=Field(...,min_length=3,max_length=100,description="Branch nmae must be between 3 and 100 characters.")
    aadhar_card:str=Field(...,min_length=12,max_length=12,regex="^\d{12}$",description="Aadhar card number must be exactly 12 digits.")
    pan_card:str=Field(...,min_length=10,max_length=10,regex="^[A-Z]{5}[0-9]{4}[A-Z]{1}$",description="PAN card must follow the standard format (e.g.,ABCDE1234F).")

    @validator("password")
    def validate_password(cls, value):
        """Enforce strong password rules."""
        if not re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", value):
            raise ValueError("Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character.")
        return value

    @validator("account_number")
    def validate_account_number(cls,value):
        if not value.isdigit():
            raise ValueError("Account number must contain only digits.")
        return value
    
    @validator("ifsc_code")
    def validate_ifsc_code(cls,value):
        if not(value[:4].isalpha() and value[4:].isdigit()):
            raise ValueError("IFSC code must have the first 4 characters as letters and the remaining 7 as digits.")
        return value.upper()
    
    @validator("aadhar_card")
    def validate_aadhar_card(cls,value):
        if not value.isdigit():
            raise ValueError("Aadhar card number must contain only digits.")
        return value
    
    @validator("pan_card")
    def validate_pan_card(cls,value):
        if not (value[:5].isalpha() and value[5:9].isdigit() and value[9].isalpha()):
            raise ValueError("PAN card format is invalid. It should be in the format ABCDE1234F.")
        return value.upper()
   
class UpdateVendorInputSchema(SQLModel):
    name:str = None
    username:str = None
    emp_id:str | None = None
    email:str = None
    mobile_number:str = None
    vendor_name:str = None
    description:str | None = None
    bank_name:str | None = None
    account_holder_name:str | None = None
    account_number:str | None = None
    ifsc_code:str | None = None
    branch_name:str | None = None
    aadhar_card:str | None = None
    pan_card:str | None = None


class ClaimRequest(SQLModel):
    points: int

class ClaimResponse(SQLModel):
    id: str
    vendor_id: str
    points: int
    status: str
    created_at: datetime
    updated_at: datetime | None

class ClaimUpdate(SQLModel):
    approved_points: int
    transaction_reference_id:str 
    


