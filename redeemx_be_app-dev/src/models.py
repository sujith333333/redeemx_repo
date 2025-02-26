from sqlmodel import SQLModel, Field, Relationship, TEXT, Column
import uuid
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
from typing import Optional
from pydantic import EmailStr

class BaseModel(SQLModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("Asia/Kolkata")))

