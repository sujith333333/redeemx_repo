from fastapi import APIRouter, Response, Request,Query
from sqlmodel import Session, select, or_,func
import uuid
from datetime import datetime,timedelta,date
import calendar


from src.response import RestResponse
from src.database import session
from src.user.models import User
from src.transaction.models import Transaction
from src.user.utils import hash_password, verify_password
from src.auth.dependencies import auth_user
from src.user.schemas import ChangePasswordSchema,UserUpdate,TransactionUserSchema
from src.user.schemas import TransactionUserSchema
from src.vendor.models import Vendor
from src.logging_config import logger


router = APIRouter()


@router.post('/register')
def user_create(user: User, response: Response, request: Request, session=session, auth_user=auth_user):
    request_info = f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"User registration attempt - Request: {request_info}, IP: {user_ip}")
    
    if auth_user.get("is_admin"):
        user_mail = session.exec(select(User).where(or_(User.email == user.email, User.emp_id == user.emp_id))).first()
        if user_mail:
            response.status_code = 400
            logger.error(f"User registration failed - Request: {request_info}, IP: {user_ip}, Reason: {user_mail.email}/{user_mail.emp_id} already exists")
            return RestResponse(error=f"{user_mail.email}/{user_mail.emp_id} is already exists")
        
        user.password = hash_password(user.password)
        user.is_user = True
        session.add(user)
        session.commit()
        session.refresh(user)
        response.status_code = 201
        response_data = user.dict()
        response_data.pop("password")
        logger.info(f"User registration successful - Request: {request_info}, IP: {user_ip}, Data: {response_data}")
        return RestResponse(data=response_data, message="User Registered successfully")
    
    response.status_code = 401
    logger.error(f"Unauthorized user registration - Request: {request_info}, IP: {user_ip}, Reason: Not authorized")
    return RestResponse(error="Your not authorized")



@router.get("/get_all/users")
def get_all_users(response: Response, request: Request, session=session, auth_user=auth_user):
    request_info = f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"Fetch all users attempt - Request: {request_info}, IP: {user_ip}")
    
    if auth_user.get("is_admin"):
        users = session.exec(select(User).where(User.is_user == True)).all()
        response_data = users if users else []
        logger.info(f"Fetch all users successful - Request: {request_info}, IP: {user_ip}, Data count: {len(response_data)}")
        return RestResponse(data=response_data)
    
    response.status_code = 401
    logger.error(f"Unauthorized access to fetch users - Request: {request_info}, IP: {user_ip}, Reason: Not authorized")
    return RestResponse(error="You are not authorized")



@router.patch('/change-password')
def user_change_password(data: ChangePasswordSchema,request:Request, response:Response, session=session, auth_user=auth_user):
    request_info = f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"Password change attempt - Request: {request_info}, IP: {user_ip}")
    
    get_user = session.get(User, uuid.UUID(auth_user.get("user_id")))
    if not get_user:
        response.status_code = 404
        logger.error(f"Password change failed - Request: {request_info}, IP: {user_ip}, Reason: User not found")
        return RestResponse(error="User not found")
    
    if not verify_password(data.old_password, get_user.password):
        response.status_code = 400
        logger.error(f"Password change failed - Request: {request_info}, IP: {user_ip}, Reason: Incorrect current password")
        return RestResponse(error="Incorrect current password")
    
    get_user.password = hash_password(data.new_password)
    session.commit()
    session.refresh(get_user)
    logger.info(f"Password change successful - Request: {request_info}, IP: {user_ip}")
    return RestResponse(message="Password updated successfully")


  
@router.get("/recent-transactions")
def get_recent_transaction(response: Response,request:Request,                    
    start_date: datetime = Query(None, description="Start date for the transactions"),
    end_date: datetime = Query(None, description="End date for the transactions"),
    session=session, auth_user=auth_user):
    
    request_info =  f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"Fetching recent transactions - Request: {request_info}, IP: {user_ip}")
    
    today = date.today()

    if start_date is None and end_date is None:
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
    
    if start_date is not None and end_date is not None and start_date > end_date:
        response.status_code = 400
        logger.error(f"Invalid date range - Request: {request_info}, IP: {user_ip}, Reason: Start date after end date")
        return RestResponse(error="Start date cannot be after end date.")
    
    if start_date is not None and end_date is None:
        end_date = datetime.combine(today, datetime.max.time())
    
    elif start_date is None and end_date is not None:
        start_date = datetime(2000, 1, 1)
    
    elif start_date is not None and end_date is not None:
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())

    transaction_query = (
        select(Transaction, Vendor.vendor_name)
        .join(Vendor, Vendor.id == Transaction.vendor_id, isouter=True) 
        .where(Transaction.user_id == auth_user.get("user_id"),
               Transaction.created_at >= start_date,
               Transaction.created_at <= end_date)
        .order_by(Transaction.created_at.desc())
    )
    transactions = session.exec(transaction_query).all()
    all_transactions = [
        
        TransactionUserSchema(
            name=trans[1] if trans[1] else "Admin", 
            date=trans[0].created_at, 
            points=trans[0].points,
            description= str(trans[0].description)
            
        ) for trans in transactions
    ]
    
    logger.info(f"Recent transactions fetched successfully - Request: {request_info}, IP: {user_ip}, Transactions count: {len(all_transactions)}")
    return RestResponse(data=all_transactions)


@router.get('/credit-transactions')
def get_credit_transaction(response: Response,request:Request, start_date: datetime = Query(None, 
                        description="Start date for the transactions"),
    end_date: datetime = Query(None, description="End date for the transactions"),
    session=session, auth_user=auth_user):
    
    request_info =  f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"Fetching credit transactions - Request: {request_info}, IP: {user_ip}")
    
    today = date.today()
    
    if start_date is None and end_date is None:
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
    
    if start_date is not None and end_date is not None and start_date > end_date:
        response.status_code = 400
        logger.error(f"Invalid date range - Request: {request_info}, IP: {user_ip}, Reason: Start date after end date")
        return RestResponse(error="Start date cannot be after end date.")
    
    if start_date is not None and end_date is None:
        end_date = datetime.combine(today, datetime.max.time())
    
    elif start_date is None and end_date is not None:
        start_date = datetime(2000, 1, 1)
    
    elif start_date is not None and end_date is not None:
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())

    credited = session.exec(
        select(Transaction).where(Transaction.user_id == auth_user.get("user_id"), Transaction.points > 0,
        Transaction.created_at >= start_date, Transaction.created_at <= end_date)
        .order_by(Transaction.created_at.desc())).all()
    
    credited_points = [TransactionUserSchema(name="Admin", date=credit.created_at, points=credit.points,description=credit.description) for credit in credited]
    
    logger.info(f"Credit transactions fetched successfully - Request: {request_info}, IP: {user_ip}, Transactions count: {len(credited_points)}")
    return RestResponse(data=credited_points)


@router.get("/all/points")
def all_points(
    response: Response,
    request: Request,
    day: datetime = Query(None, description="Fetch data on particular date (YYYY-MM-DD)"),
    start_date: datetime = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: datetime = Query(None, description="End date in YYYY-MM-DD format"),
    month: int = Query(None, description="Month number (1-12)"),
    year: int = Query(None, description="Year (e.g., 2024)"),
    session=session,
    auth_user=auth_user
):
    request_info = f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"Fetch all points - Request: {request_info}, IP: {user_ip}")
    
    if not auth_user.get("user_id"):
        response.status_code = 401
        logger.error(f"Unauthorized access - Request: {request_info}, IP: {user_ip}, Reason: User not authenticated")
        return RestResponse(error="You are not authenticated")
    
    today = date.today()
    
    if start_date is None and end_date is None and month is None and year is None and day is None:
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
    elif day is not None:
        start_date = datetime.combine(day, datetime.min.time())
        end_date = datetime.combine(day, datetime.max.time())
    
    if start_date is not None and end_date is not None and start_date > end_date:
        response.status_code = 400
        logger.error(f"Invalid date range - Request: {request_info}, IP: {user_ip}, Reason: Start date cannot be after end date")
        return RestResponse(error="Start date cannot be after end date.")
    
    elif month is not None and year is not None:
        if not (1 <= month <= 12):
            response.status_code = 400
            logger.error(f"Invalid month input - Request: {request_info}, IP: {user_ip}, Reason: Invalid month {month}")
            return RestResponse(error="Invalid month. Must be between 1 and 12.")
        
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        start_date = first_day
        end_date = last_day
    
    user_id = session.exec(select(User.id).where(User.id == auth_user.get("user_id"))).first()
    
    if not user_id:
        logger.error(f"User not found - Request: {request_info}, IP: {user_ip}, Reason: User details not found")
        return RestResponse(error="User details not found")
    
    total_points = session.exec(
        select(func.sum(Transaction.points)).where(Transaction.user_id == user_id)
    ).first()
    
    total_credited_points = session.exec(
        select(func.sum(Transaction.points)).where(
            Transaction.user_id == user_id,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date,
            Transaction.points > 0
        )
    ).first()
    
    total_debited_points = session.exec(
        select(func.sum(Transaction.points)).where(
            Transaction.user_id == user_id,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date,
            Transaction.points < 0
        )
    ).first()
    
    reports = [
        {
            "balance":(total_points) if total_points else 0,
            "credited":abs(total_credited_points) if total_credited_points else 0,
            "debited":abs(total_debited_points) if total_debited_points else 0
        }
    ]
    
    logger.info(f"Points retrieval successful - Request: {request_info}, IP: {user_ip}, Data: {reports}")
    return RestResponse(data=reports)


@router.get('/debit-transactions')
def get_debit_transaction(response:Response,request: Request, start_date: datetime = Query(None, 
                        description="Start date for the transactions"),
    end_date: datetime = Query(None, description = "End date for the transactions"),
    session= session,auth_user=auth_user, ):

    request_info = f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"Debit transaction retrieval - Request: {request_info}, IP: {user_ip}")

    today = date.today()

    if start_date is None and end_date is None :
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
 
    if start_date is not None and end_date is not None and start_date > end_date:
        response.status_code=400
        logger.error(f"Invalid date range - Request: {request_info}, IP: {user_ip}, Reason: Start date cannot be after end date")
        return RestResponse(error="Start date cannot be after end date.")
   
    if start_date is not None and end_date is None:
        end_date = datetime.combine(today, datetime.max.time())
  
    elif start_date is None and end_date is not None:
        start_date = datetime(2000, 1, 1)
 
    elif start_date is not None and end_date is not None:
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())
        
    debited_query = (
        select(Transaction).where(Transaction.user_id == auth_user.get("user_id"), Transaction.points < 0,
        Transaction.created_at>=start_date,Transaction.created_at<=end_date)
        .order_by(Transaction.created_at.desc()))

    
    debited = session.exec(debited_query).all()
    debited_points = [{
        "name":"Admin" if transaction.vendor_id is None else session.exec(
            select(Vendor.vendor_name).where(Vendor.id == transaction.vendor_id)
        ).first(),
        "date":transaction.created_at,
        "points":transaction.points,
        "description":transaction.description
    }for transaction in debited]
    logger.info(f"Debit transactions retrieved - Request: {request_info}, IP: {user_ip}, Total Transactions: {len(debited_points)}")
    
    return RestResponse(data = debited_points)


@router.get("/vendor/details")
def get_vendor_details(response: Response, request: Request, session=session, auth_user=auth_user):
    request_info = f"{request.method}:{request.url.path} user:{auth_user.get('user_id')}"
    user_ip = request.client.host
    logger.info(f"Vendor details request - Request: {request_info}, IP: {user_ip}")
    
    if not auth_user.get("user_id"):
        response.status_code = 403
        logger.error(f"Unauthorized access attempt - Request: {request_info}, IP: {user_ip}, Reason: User not authenticated")
        return RestResponse(error="You are not authenticated")
    
    vendor_details = session.exec(select(Vendor.vendor_name)).all()
    logger.info(f"Vendor details retrieved successfully - Request: {request_info}, IP: {user_ip}, Count: {len(vendor_details)}")
    
    return RestResponse(data=vendor_details)

 
@router.delete("/delete-user/{user_id}")
def delete_user(user_id: str, response:Response,request:Request,session=session,auth_user=auth_user):
    if auth_user.get("is_admin"):
        db_user = session.exec(select(User).where(User.id == user_id)).first()
        if not db_user:
            response.status_code = 400
            return RestResponse(error= "User not found")
        session.delete(db_user)
        session.commit()
        return RestResponse(message = "User deleted successfully")


    response.status_code = 401
    return RestResponse(error ="You are not authorized")


@router.patch("/update-user/{user_id}")
def update_user(user_id:str,user_update:UserUpdate,response:Response,request:Request,session=session,auth_user=auth_user):
    if auth_user.get("is_admin"):
        db_user = session.exec(select(User).where(User.id == user_id)).first()
        if not db_user:
            response.status_code = 400
            return RestResponse(error = "User not found")
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return RestResponse(data= db_user,message="User updated successfully")
    response.status_code = 401
    return RestResponse(error ="Your not authorized")