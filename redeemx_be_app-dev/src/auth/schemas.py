from sqlmodel import SQLModel


class UserLoginSchema(SQLModel):
    email:str | None = None
    emp_id:str | None = None
    password:str