from sqlmodel import Field, Relationship
import uuid
from typing import Optional

from src.models import BaseModel



class Transaction(BaseModel, table=True):
    points:int = Field(...)
    user_id:Optional[str] = Field(None, foreign_key="user.id")
    vendor_id:Optional[str] = Field(None, foreign_key="vendor.id")
    description:Optional[str] = Field(None)

    user_transaction:Optional["User"] = Relationship(back_populates="user_transaction_details")
    vendor_transaction:Optional["Vendor"] = Relationship(back_populates="vendor_transaction_details")

# class reports(BaseModel, table=True):
#     Points_redeemed_by_employees=Field(...)
#     Vendor_balance_points=int=Field(...)
#     Points_redeemed_by_vendor=Field(...)
#     claim_id:Optional[str] = Field(None, foreign_key="claim_id")

#     vendor_claim:Optional["Claim"] =Relationship(back_populates="vendor_claims")