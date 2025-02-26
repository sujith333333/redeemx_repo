from sqlmodel import SQLModel
from fastapi import Response
from datetime import date

from src.response import RestResponse

class TransactionInputSchema(SQLModel):
    points:int
    user_id:str | None = None
    vendor_id:str | None = None

class TransactionUserInputSchema(SQLModel):
    vendor_name:str
    points:int
    user_id:str | None = None
    vendor_id:str | None = None
    description:str | None = None

        