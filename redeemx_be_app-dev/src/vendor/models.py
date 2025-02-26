from sqlmodel import Field, Relationship, Column, TEXT
import uuid
from typing import Optional, List
from pydantic import EmailStr,validator

from src.transaction.models import Transaction
from src.models import BaseModel
from src.user.models import User
from datetime import datetime
from sqlalchemy import Enum as SAEnum


class Vendor(BaseModel, table=True):
    vendor_name: str = Field(..., 
                             unique=True, 
                             min_length=3, 
                             max_length=100,
                             description="Vendor name must be unique and between 3 and 100 characters.")
    
    description: Optional[str] = Field(None, 
                                       max_length=500,
                                       description="An optional description with a maximum of 500 characters.")
    
    qr_code:str  = Field(sa_column=Column(TEXT),
                         min_length=5, 
                         description="A mandatory QR code string with at least 5 characters.")
    
    user_id: Optional[str] = Field(None, 
                                         foreign_key="user.id", 
                                         unique=True,
                                         description="An optional unique UUID that references the user table.")
    
    bank_name:str=Field(...,max_length=100,description="Bank name with a maximum of 100 characters.")
    account_holder_name:str=Field(...,max_length=100,description="Account holder's name with a maximum of 100 characters.")
    account_number:str=Field(...,min_length=8,max_length=20,description="Account number must be between 8 and 20 digits.")
    ifsc_code:str=Field(...,min_length=11,max_length=11,description="IFSC code must be exactly 11 characters.")
    branch_name:str=Field(...,max_length=100,description="Branch name with a maximum of 100 characters.")

    aadhar_card:str=Field(...,min_length=12,max_length=12,description="Aadhar card number must be exactly 12 digits.")
    pan_card: str=Field(...,min_length=10,max_length=10,description="PAN card number must be exactly 10 characters.")

    # Relationships
    user: Optional["User"] = Relationship(back_populates="vendor_details")
    vendor_transaction_details: List["Transaction"] = Relationship(back_populates="vendor_transaction")
    claims: List["Claim"] = Relationship(back_populates="vendor")

class Claim(BaseModel, table=True):
    vendor_id: str = Field(foreign_key="vendor.id") 
    points: int
    status: str = Field(default="PENDING",sa_column=Column(SAEnum("PENDING", "APPROVED", "REJECTED", name="claim_status"), default="PENDING"))
    updated_at: Optional[datetime] = Field(default=None) 
    admin_name: Optional[str] = Field(default=None, max_length=255)  
    transaction_reference_id: Optional[str] = Field(default=None, max_length=50)
    vendor: "Vendor" = Relationship(back_populates="claims")

    def validate_points(cls,value:int) -> int:
        if value <=0:
            raise ValueError("Points must be greater than 0.")
        return value
    
    def __init__(self,**data):
        super().__init__(**data)
        self.validate_points(self.points)

class DailyReports(BaseModel, table=True):
    points_redeemed_by_employees:int=Field(default=0)
    vendor_balance_points:int=Field(default=0)
    points_redeemed_by_vendor:int=Field(default=0)