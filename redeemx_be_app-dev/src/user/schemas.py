from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import BaseModel, Field, validator,EmailStr
from typing import Optional

class ChangePasswordSchema(SQLModel):
    old_password:str
    new_password:str

  
class TransactionUserSchema(SQLModel):
    name: str  
    points: int
    date: datetime
    description: str | None = None


class UserUpdate(SQLModel):
    username: str = None
    name: str = None
    email: EmailStr = None
    emp_id: str = None
    mobile_number: str = None
    
