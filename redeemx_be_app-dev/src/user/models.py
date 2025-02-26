from sqlmodel import Field, Relationship
from pydantic import EmailStr
from typing import Optional, List


from src.models import BaseModel



class User(BaseModel, table=True):
    username: str = Field(..., 
                          min_length=3, 
                          max_length=30, 
                          regex=r"^[a-zA-Z0-9_.-]+$", 
                          description="Username must be 3-30 characters long and contain only letters, numbers, underscores, dots, or hyphens.")
    
    name: str = Field(..., 
                      min_length=3, 
                      max_length=50, 
                      description="Name must be between 3 and 50 characters long.")
    
    password: str = Field(..., 
                          min_length=8, 
                          description="Password must be at least 8 characters long.")
    
    email: EmailStr = Field(..., 
                            unique=True, 
                            description="A valid and unique email address.")
    
    emp_id: Optional[str] = None
    
    mobile_number: str = Field(..., 
                               
                               description="A 10-digit valid mobile number.")
    
    is_vendor: bool = Field(default=False,
                            description="Boolean flag to indicate if the user is a vendor.")
    
    is_user: bool = Field(default=False, 
                          description="Boolean flag to indicate if the user is a regular user.")
    
    is_admin: bool = Field(default=False, 
                           description="Boolean flag to indicate if the user is an admin.")

    # Relationships
    vendor_details: Optional["Vendor"] = Relationship(back_populates="user")
    user_transaction_details: List["Transaction"] = Relationship(back_populates="user_transaction")

    class Config:
        validate_assignment = True
    
    def validate_password_strength(cls, value):
        if len(value) < 8 or not any(char.isdigit() for char in value) or not any(char.isupper() for char in value):
            raise ValueError("Password must be at least 8 characters long, contain at least one digit, and one uppercase letter.")
        return value

    def validate_mobile_number(cls, value):
        if not str(value).isdigit():
            raise ValueError("Mobile number must contain only digits.")
        if len(str(value)) != 10:
            raise ValueError("Mobile number must be exactly 10 digits long.")
        return value

    def __init__(self, **data):
        super().__init__(**data)
        self.validate_password_strength(self.password)
        self.validate_mobile_number(self.mobile_number)


