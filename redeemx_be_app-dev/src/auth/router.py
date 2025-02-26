from fastapi import APIRouter, Response, Request
from sqlmodel import Session, select, or_
from typing import Annotated,Any
import os
from src.database import session
from dotenv import load_dotenv


from src.user.models import User
from src.response import RestResponse
from src.user.utils import verify_password
from src.auth.utils import create_access_token
from src.auth.schemas import UserLoginSchema
from src.logging_config import logger

load_dotenv()

router = APIRouter()


@router.post('/login')
def user_login(user: UserLoginSchema, request:Request, response:Response, session=session):
    request_info = f"{request.method} {request.url.path}"
    logger.info(f"Login attempt - Request: {request_info}, User: {user.email}:{user.emp_id}, IP: {request.client.host}")
    db_user = session.exec(select(User).where(or_(User.email==user.email, User.emp_id==user.emp_id))).first()
    if not db_user:
        logger.error(f"Failed login - Request: {request_info}, User: {user.email}:{user.emp_id}, Reason: Invalid Email/Employee ID")
        response.status_code = 400
        return RestResponse(error="Invalid Email/Employee Id")
    
    if not verify_password(user.password, db_user.password):
        logger.error(f"Failed login - Request: {request_info}, User: {user.email}:{user.emp_id}, Reason: Invalid Password")
        response.status_code = 400
        return RestResponse(error="Invalid Password")
    
    token = create_access_token(data={"email":db_user.email, 
                                      "user_id":str(db_user.id), 
                                      "is_admin":db_user.is_admin, 
                                      "is_user":db_user.is_user,
                                      "is_vendor":db_user.is_vendor, 
                                      })
    user_type = ""
    if db_user.is_admin:
        user_type = "admin"
    elif db_user.is_vendor:
        user_type = "vendor"
    else:
        user_type = "user"
    logger.info(f"Successful login - Request: {request_info}, User: {db_user.email}, User Type: {user_type}")
    return RestResponse(data={"token":token, "user_type":user_type}, message="Login success")
