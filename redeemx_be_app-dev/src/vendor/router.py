from fastapi import APIRouter, Response, Request,Query,Depends
from sqlmodel import Session, select, or_, func
import uuid
from datetime import datetime,date,timedelta
import calendar
from typing import Optional


from src.response import RestResponse
from src.database import session,get_session
from src.user.models import User
from src.vendor.models import Vendor,Claim,DailyReports
from src.transaction.models import Transaction
from src.user.utils import hash_password, verify_password
from src.auth.dependencies import auth_user
from src.vendor.schemas import VendorInputSchema,UpdateVendorInputSchema
from src.vendor.utils import create_vendor_with_qr_code
from src.vendor.schemas import ClaimRequest, ClaimResponse, ClaimUpdate
from src.pagination import get_pagination_params
from src.logging_config import logger

router = APIRouter()

@router.post("/register")
def vendor_creation(vendor:VendorInputSchema, request:Request, response:Response, session=session, auth_user=auth_user):
    request_info = f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"Vendor registration - Request: {request_info}, Vendor: {vendor}, IP: {user_ip}")
    if auth_user.get("is_admin"):
        user_mail = session.exec(select(User).where(User.email == vendor.email)).first()
        if user_mail:
            response.status_code = 400
            logger.error(f"Vendor registration failed - Request: {request_info}, Vendor: {vendor}, IP: {user_ip},Reason: user_email is already exists")
            return RestResponse(error=f"{user_mail.email} is already exists")
        user = User(
            name = vendor.name,
            username = vendor.username,
            email = vendor.email,
            password = hash_password(vendor.password),
            emp_id = vendor.emp_id if vendor.emp_id else None,
            mobile_number = vendor.mobile_number,
            is_vendor=True
        )
        session.add(user)

        add_vendor = Vendor(
            vendor_name = vendor.vendor_name,
            description = vendor.description,
            qr_code =  create_vendor_with_qr_code(vendor.vendor_name),
            user_id = user.id,
            bank_name=vendor.bank_name,
            account_holder_name=vendor.account_holder_name,
            account_number=vendor.account_number,
            ifsc_code=vendor.ifsc_code,
            branch_name=vendor.branch_name,
            aadhar_card=vendor.aadhar_card,
            pan_card=vendor.pan_card
        )
        session.add(add_vendor)
        session.commit()
        session.refresh(add_vendor)
        response.status_code = 201
        vendor_data = vendor.dict()
        vendor_data.pop("password", None)
        logger.info(f"Vendor registration successful - Request: {request_info}, Vendor: {vendor}, IP: {user_ip}")
        return RestResponse(data=vendor_data, message="Vendor registered successfully")
    logger.error(f"Unauthorized vendor registration - Request: {request_info}, User: {auth_user.get('email')}, IP: {user_ip}, Reason: You are not authorized")
    response.status_code = 401
    return RestResponse(error="You are not authorized")


@router.get("/get_all/vendors")
def get_all_vendors(response:Response, request:Request, session=session, auth_user=auth_user):
    request_info = f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"Get all vendors request received - Request: {request_info}, IP: {user_ip}")
    if auth_user.get("is_admin"):
        users = session.exec(select(User).where(User.is_vendor == True)).all()
        response_data = users if users else [] 
        logger.info(f"Vendors retrieved successfully - Request: {request_info}, IP: {user_ip}")
        return RestResponse(data=response_data)
    
    logger.error(f"Unauthorized access - Request: {request_info}, User: {auth_user.get('email')}, IP: {user_ip}, Reason: You are not authorized")
    response.status_code = 401
    return RestResponse(error="Your not unauthorized")


# @router.put("/update-vendor/{vendor_id}")
# def update_vendor(
#     vendor_id: str,
#     vendor_update: UpdateVendorInputSchema,
#     response: Response,
#     session=session,
#     auth_user=auth_user
# ):
#     if not auth_user.get("is_admin"):
#         response.status_code = 401
#         return RestResponse(error="You are not authorized")

#     vendor = session.exec(select(Vendor).where(Vendor.id == vendor_id)).first()
#     if not vendor:
#         response.status_code = 400
#         return RestResponse(error="Vendor not found")

#     user = session.exec(select(User).where(User.id == vendor.user_id)).first()
#     if not user:
#         response.status_code = 400
#         return RestResponse(error="Associated user not found")

#     update_data = vendor_update.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         if hasattr(user, key):  
#             setattr(user, key, value)
#         elif hasattr(vendor, key): 
#             setattr(vendor, key, value)

#     session.add(user)
#     session.add(vendor)
#     session.commit()
#     session.refresh(vendor)

#     return RestResponse(data=update_data, message="Vendor updated successfully")


# @router.delete("/delete-vendor/{vendor_id}")
# def delete_vendor(
#     vendor_id: str,
#     response: Response,
#     session=session,
#     auth_user=auth_user
# ):
#     if not auth_user.get("is_admin"):
#         response.status_code = 401
#         return RestResponse(error="You are not authorized")

#     vendor = session.exec(select(Vendor).where(Vendor.id == vendor_id)).first()
#     if not vendor:
#         response.status_code = 400
#         return RestResponse(error="Vendor not found")

#     user = session.exec(select(User).where(User.id == vendor.user_id)).first()
#     session.delete(vendor)
#     if user:
#         session.delete(user)
#     session.commit()
#     return RestResponse(message="Vendor and associated user deleted successfully")


@router.get("/get/vendors-details")
def get_vendor_details(response:Response, request:Request, session=session, auth_user=auth_user):
    request_info = f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"- Request: {request_info}, IP: {user_ip}")
    vendor_details = session.exec(select(Vendor, User).join(User).where(Vendor.user_id == auth_user.get("user_id"))).first()
    if not vendor_details:
        response.status_code = 400
        logger.error(f"Vendor details not found: {auth_user['user_id']}")
        return RestResponse(error="Vendor details not found")
    vendor, user = vendor_details
    
    response_data = {
        "vendor": vendor.dict(),  
        "user": user.dict(exclude={"password"})
    }
    logger.info(f"Vendor details retrieved successfully: {auth_user['user_id']}")
    return RestResponse(data=response_data) 

@router.get("/user/transactions")
def get_vendor_user_transactions(
    response:Response,
    request:Request,
    start_date: datetime = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: datetime = Query(None, description="End date in YYYY-MM-DD format"),
    month: int = Query(None, description="Month number (1-12)"),
    year: int = Query(None, description="Year (e.g., 2024)"),
    session=session,
    auth_user=auth_user,
    pagination: dict = Depends(get_pagination_params) 
):
    limit = pagination["limit"]
    offset = pagination["offset"]
    
    today = date.today()
    first_transaction_date = session.exec(select(func.min(Transaction.created_at))).first()

    request_info = f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"- Request: {request_info}, IP: {user_ip}")

    if start_date is None and end_date is None and month is None and year is None:
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
        logger.info("No date filters provided. Defaulting to today's date range.")

    if start_date is not None and end_date is not None and start_date > end_date:
        response.status_code=400
        logger.error(f"Invalid date range: Start date ({start_date}) is after end date ({end_date}).")
        return RestResponse(error="Start date cannot be after end date.")
    
    if start_date is not None and end_date is None:
        end_date = datetime.combine(today, datetime.max.time())
        logger.info(f"End date not provided. Defaulting to end of today: {end_date}.") 

    elif start_date is None and end_date is not None:
        start_date = first_transaction_date
        end_date = datetime.combine(end_date, datetime.max.time())
        logger.info(f"Start date not provided. Defaulting to first transaction date: {start_date}.") 

    elif start_date is not None and end_date is not None:
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())
        logger.info(f"Date range set: {start_date} to {end_date}.")  

    elif month is not None and year is not None:
        if not (1 <= month <= 12):
            response.status_code=400
            logger.error(f"Invalid month provided: {month}. Must be between 1 and 12.")
            return RestResponse(error="Invalid month. Must be between 1 and 12.")
                
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        start_date = first_day
        end_date = last_day
        logger.info(f"Month and year provided. Date range set: {start_date} to {end_date}.")

    vendor_id = session.exec(
        select(Vendor.id).where(Vendor.user_id == auth_user.get("user_id"))
    ).first()
     
    if not vendor_id:
        logger.error(f"Vendor details not found: {auth_user['user_id']}")
        return RestResponse(error="Vendor details not found")

    query = (
        select(Transaction)
        .where(
            Transaction.vendor_id == vendor_id,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date)
        .order_by(Transaction.created_at.desc())
        .offset(offset)
        .limit(limit)
        )
    all_user_transactions=session.exec(query).all()

    if not all_user_transactions:
        logger.info(f"No transactions found for vendor ID: {vendor_id} within the specified date range.")
        return RestResponse(data=[], message="No transactions found for the given criteria.")
    
    total_records_query = select(func.count()).where(
            Transaction.vendor_id == vendor_id,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date,
            Transaction.user_id != None )
    
    total=session.exec(total_records_query).first()

    reports = [
        {
            "user": session.exec(
                select(User.name).where(User.id == transaction.user_id)
            ).first(),
            "points": transaction.points*(-1),
            "date": transaction.created_at
        }
        for transaction in all_user_transactions if transaction.user_id is not None
    ]
    logger.info(f"Successfully retrieved {len(reports)} transactions for vendor ID: {vendor_id}.")
    return RestResponse(data=reports,metadata={"total":total,"limit":limit,"offset":offset})
    

@router.get("/admin/transactions")
def get_vendor_admin_transactions(
    response:Response,
    request:Request,
    start_date: datetime = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: datetime = Query(None, description="End date in YYYY-MM-DD format"),
    month: int = Query(None, description="Month number (1-12)"),
    year: int = Query(None, description="Year (e.g., 2024)"),
    session=session,
    auth_user=auth_user
):
    today = date.today()
    first_transaction_date = session.exec(select(func.min(Transaction.created_at))).first()

    request_info = f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"- Request: {request_info}, IP: {user_ip}")

    if start_date is None and end_date is None and month is None and year is None:
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
        logger.info("No date filters provided. Defaulting to today's date range.")

    if start_date is not None and end_date is not None and start_date > end_date:
        response.status_code=400
        logger.error(f"Invalid date range: Start date ({start_date}) is after end date ({end_date}).")
        return RestResponse(error="Start date cannot be after end date.")
    
    if start_date is not None and end_date is None:
        end_date = datetime.combine(today, datetime.max.time())
        logger.info(f"End date not provided. Defaulting to end of today: {end_date}.") 

    elif start_date is None and end_date is not None:
        start_date = first_transaction_date
        end_date = datetime.combine(end_date, datetime.max.time())
        logger.info(f"Start date not provided. Defaulting to first transaction date: {start_date}.") 

    elif start_date is not None and end_date is not None:
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())
        logger.info(f"Date range set: {start_date} to {end_date}.")  

    elif month is not None and year is not None:
        if not (1 <= month <= 12):
            response.status_code=400
            logger.error(f"Invalid month provided: {month}. Must be between 1 and 12.")
            return RestResponse(error="Invalid month. Must be between 1 and 12.")
                
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        start_date = first_day
        end_date = last_day
        logger.info(f"Month and year provided. Date range set: {start_date} to {end_date}.")

    vendor_id = session.exec(
        select(Vendor.id).where(Vendor.user_id == auth_user.get("user_id"))
    ).first()
     
    if not vendor_id:
        logger.error(f"Vendor details not found: {auth_user['user_id']}")
        return RestResponse(error="Vendor details not found")

    all_admin_transactions = session.exec(
        select(Transaction)
        .where(
            Transaction.vendor_id == vendor_id,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date)
        .order_by(Transaction.created_at.desc())    

    ).all()

    if not all_admin_transactions:
        logger.info(f"No admin transactions found for vendor ID: {vendor_id} within the specified date range.")
        return RestResponse(data=[], message="No transactions found for the given criteria.")

    reports = [
        {
            "user": "admin",
            "points": transaction.points*(-1),
            "date": transaction.created_at
        }
        for transaction in all_admin_transactions if transaction.user_id is None 
    ]
    logger.info(f"Successfully retrieved {len(reports)} admin transactions for vendor ID: {vendor_id}.")
    return RestResponse(data=reports)


@router.get("/all/transactions")
def get_vendor_all_transactions(
    response:Response,
    request:Request,
    start_date: datetime = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: datetime = Query(None, description="End date in YYYY-MM-DD format"),
    month: int = Query(None, description="Month number (1-12)"),
    year: int = Query(None, description="Year (e.g., 2024)"),
    session=session,
    auth_user=auth_user,
    pagination: dict = Depends(get_pagination_params)
):
    limit = pagination["limit"]
    offset = pagination["offset"]
    
    today = date.today()
    first_transaction_date = session.exec(select(func.min(Transaction.created_at))).first()

    request_info = f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"- Request: {request_info}, IP: {user_ip}")

    if start_date is None and end_date is None and month is None and year is None:
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
        logger.info("No date filters provided. Defaulting to today's date range.")

    if start_date is not None and end_date is not None and start_date > end_date:
        response.status_code=400
        logger.error(f"Invalid date range: Start date ({start_date}) is after end date ({end_date}).")
        return RestResponse(error="Start date cannot be after end date.")
    
    if start_date is not None and end_date is None:
        end_date = datetime.combine(today, datetime.max.time())
        logger.info(f"End date not provided. Defaulting to end of today: {end_date}.") 

    elif start_date is None and end_date is not None:
        start_date = first_transaction_date
        end_date = datetime.combine(end_date, datetime.max.time())
        logger.info(f"Start date not provided. Defaulting to first transaction date: {start_date}.")  

    elif start_date is not None and end_date is not None:
        start_date = datetime.combine(start_date, datetime.min.time())
        end_date = datetime.combine(end_date, datetime.max.time())
        logger.info(f"Date range set: {start_date} to {end_date}.")  

    elif month is not None and year is not None:
        if not (1 <= month <= 12):
            response.status_code=400
            logger.error(f"Invalid month provided: {month}. Must be between 1 and 12.")
            return RestResponse(error="Invalid month. Must be between 1 and 12.")
                
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        start_date = first_day
        end_date = last_day
        logger.info(f"Month and year provided. Date range set: {start_date} to {end_date}.")
    logger.info(f"Final date range: {start_date} to {end_date}")

    vendor_id = session.exec(
        select(Vendor.id).where(Vendor.user_id == auth_user.get("user_id"))
    ).first()
     
    if not vendor_id:
        logger.error(f"Vendor details not found: {auth_user['user_id']}")
        return RestResponse(error="Vendor details not found")
    
    logger.info(f"Vendor ID found: {vendor_id}")

    query = (
        select(Transaction)
        .where(
            Transaction.vendor_id == vendor_id,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date)
        .order_by(Transaction.created_at.desc())
        .limit(limit)
        .offset(offset)    
    )

    all_transactions = session.exec(query).all()

    if not all_transactions:
        logger.info(f"No transactions found for vendor ID {vendor_id} within the given date range.")
        return RestResponse(data=[], message="No transactions found for the given criteria.")
    
    logger.info(f"Retrieved {len(all_transactions)} transactions for vendor ID: {vendor_id}")
        
    total_records_query = select(func.count()).where(Transaction.vendor_id == vendor_id,
                                                     Transaction.created_at >= start_date,
                                                     Transaction.created_at <= end_date)    
    total = session.exec(total_records_query).first()
    reports = [
            {
                "user": "admin" if transaction.user_id is None else session.exec(
                    select(User.name).where(User.id == transaction.user_id)
                ).first(),               
                "points": transaction.points*(-1) if transaction.user_id is None else transaction.points*(-1),
                "date":transaction.created_at
            }
            for transaction in all_transactions
        ]
    logger.info(f"Successfully processed {len(reports)} transactions.")
    return RestResponse(data=reports, metadata={"total":total, "limit":limit, "offset":offset})


@router.get("/credited/points")
def vendor_credited_points( response:Response,
    request:Request,
    start_date: datetime = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: datetime = Query(None, description="End date in YYYY-MM-DD format"),
    day: datetime = Query(None, description="Fetch data on particular date (YYYY-MM-DD)"),
    month: int = Query(None, description="Month number (1-12)"),
    year: int = Query(None, description="Year (e.g., 2024)"),
    session=session,
    auth_user=auth_user):

    today = date.today()
    
    request_info = f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"- Request: {request_info}, IP: {user_ip}")

    if start_date is None and end_date is None and month is None and year is None and day is None:
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
        logger.info("No date filters provided. Using today's date range.")

    elif day is not None:
         start_date = datetime.combine(day, datetime.min.time()) 
         end_date = datetime.combine(day, datetime.max.time())
         logger.info(f"Fetching data for a particular date: {day}")  

    if start_date is not None and end_date is not None and start_date > end_date:
        response.status_code=400
        logger.error(f"Invalid date range: Start date ({start_date}) is after end date ({end_date}).")
        return RestResponse(error="Start date cannot be after end date.")

    elif start_date is not None and end_date is not None:
       start_date = datetime.combine(start_date, datetime.min.time()) 
       end_date = datetime.combine(end_date, datetime.max.time()) 

    elif month is not None and year is not None:
        if not (1 <= month <= 12):
            response.status_code=400
            logger.error(f"Invalid month provided: {month}. Must be between 1 and 12.")
            return RestResponse(error="Invalid month. Must be between 1 and 12.")
                        
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        start_date = first_day
        end_date = last_day
        logger.info(f"Month and year provided. Date range set: {start_date} to {end_date}")
    logger.info(f"Final date range: {start_date} to {end_date}")

    vendor_id = session.exec(
        select(Vendor.id).where(Vendor.user_id == auth_user.get("user_id"))
    ).first()
     
    if not vendor_id:
        logger.error(f"Vendor not found for user ID: {auth_user['user_id']}")
        return RestResponse(error="Vendor details not found")

    total_credited_points = session.exec(
        select(func.sum(Transaction.points))
        .where(
            Transaction.vendor_id == vendor_id,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date,
            Transaction.points<0
        )
    ).first()
    
    logger.info(f"Total credited points for vendor ID {vendor_id}: {total_credited_points}")
    reports = [
        {
            "credited": abs(total_credited_points) if total_credited_points else 0
        }
    ]
    logger.info("Successfully processed credited points request.")
    return RestResponse(data=reports)

@router.get("/debited/points/")
def vendor_debited_points( response:Response,
    request:Request,                      
    start_date: datetime = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: datetime = Query(None, description="End date in YYYY-MM-DD format"),
    day: datetime = Query(None, description="Fetch data on particular date (YYYY-MM-DD)"),
    month: int = Query(None, description="Month number (1-12)"),
    year: int = Query(None, description="Year (e.g., 2024)"),
    session=session,
    auth_user=auth_user):

    today = date.today()

    request_info = f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"- Request: {request_info}, IP: {user_ip}")

    if start_date is None and end_date is None and month is None and year is None and day is None:
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
        logger.info("No date filters provided. Using today's date range.")

    elif day is not None:
         start_date = datetime.combine(day, datetime.min.time()) 
         end_date = datetime.combine(day, datetime.max.time())
         logger.info(f"Fetching data for a particular date: {day}")  

    if start_date is not None and end_date is not None and start_date > end_date:
        response.status_code=400
        logger.error(f"Invalid date range: Start date ({start_date}) is after end date ({end_date}).")
        return RestResponse(error="Start date cannot be after end date.")

    elif start_date is not None and end_date is not None:
       start_date = datetime.combine(start_date, datetime.min.time()) 
       end_date = datetime.combine(end_date, datetime.max.time()) 

    elif month is not None and year is not None:
        if not (1 <= month <= 12):
            response.status_code=400
            logger.error(f"Invalid month provided: {month}. Must be between 1 and 12.")
            return RestResponse(error="Invalid month. Must be between 1 and 12.")
                     
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        start_date = first_day
        end_date = last_day
        logger.info(f"Month and year provided. Date range set: {start_date} to {end_date}")

    logger.info(f"Final date range: {start_date} to {end_date}")

    vendor_id = session.exec(
        select(Vendor.id).where(Vendor.user_id == auth_user.get("user_id"))
    ).first()
     
    if not vendor_id:
        logger.error(f"Vendor not found for user ID: {auth_user['user_id']}")
        return RestResponse(error="Vendor details not found")
    
    logger.info(f"Vendor ID found: {vendor_id}")
    total_debited_points = session.exec(
        select(func.sum(Transaction.points))
        .where(
            Transaction.vendor_id == vendor_id,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date,
            Transaction.points>0
        )
    ).first()

    logger.info(f"Total debited points for vendor ID {vendor_id}: {total_debited_points}")
    
    reports = [
        {
            "debited": total_debited_points*(-1) if total_debited_points else 0
        }
    ]
    logger.info("Successfully processed debited points request.")
    return RestResponse(data=reports)

@router.get("/all/points/")
def all_points( response:Response,
    request:Request,
    start_date: datetime = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: datetime = Query(None, description="End date in YYYY-MM-DD format"),
    day: datetime = Query(None, description="Fetch data on particular date (YYYY-MM-DD)"),
    month: int = Query(None, description="Month number (1-12)"),
    year: int = Query(None, description="Year (e.g., 2024)"),
    session=session,
    auth_user=auth_user):

    today = date.today()

    request_info = f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip = request.client.host
    logger.info(f"- Request: {request_info}, IP: {user_ip}")

    if start_date is None and end_date is None and month is None and year is None and day is None:
        start_date = datetime.combine(today, datetime.min.time())
        end_date = datetime.combine(today, datetime.max.time())
        logger.info("No date filters provided. Using today's date range.")

    elif day is not None:
         start_date = datetime.combine(day, datetime.min.time()) 
         end_date = datetime.combine(day, datetime.max.time())
         logger.info(f"Fetching data for a particular date: {day}")  

    if start_date is not None and end_date is not None and start_date > end_date:
        response.status_code=400
        logger.error(f"Invalid date range: Start date ({start_date}) is after end date ({end_date}).")
        return RestResponse(error="Start date cannot be after end date.")

    elif start_date is not None and end_date is not None:
       start_date = datetime.combine(start_date, datetime.min.time()) 
       end_date = datetime.combine(end_date, datetime.max.time()) 

    elif month is not None and year is not None:
        if not (1 <= month <= 12):
            response.status_code=400
            logger.error(f"Invalid month provided: {month}. Must be between 1 and 12.")
            return RestResponse(error="Invalid month. Must be between 1 and 12.")
                
        
        first_day = datetime(year, month, 1)
        last_day = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
        start_date = first_day
        end_date = last_day
        logger.info(f"Month and year provided. Date range set: {start_date} to {end_date}")

    logger.info(f"Final date range: {start_date} to {end_date}")

    vendor_id = session.exec(
        select(Vendor.id).where(Vendor.user_id == auth_user.get("user_id"))
    ).first()

    if not vendor_id:
        logger.error(f"Vendor not found for user ID: {auth_user['user_id']}")
        return RestResponse(error="Vendor details not found")
    
    total_points = session.exec(
        select(func.sum(Transaction.points))
        .where(
            Transaction.vendor_id == vendor_id
        )
    ).first()

    total_credited_points = session.exec(
        select(func.sum(Transaction.points))
        .where(
            Transaction.vendor_id == vendor_id,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date,
            Transaction.points<0
        )
    ).first()

    total_debited_points = session.exec(
        select(func.sum(Transaction.points))
        .where(
            Transaction.vendor_id == vendor_id,
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date,
            Transaction.points>0
        )
    ).first()
    
    logger.info(f"Total points balance for vendor ID {vendor_id}: {total_points}")
    logger.info(f"Total credited points for vendor ID {vendor_id}: {total_credited_points}")
    logger.info(f"Total debited points for vendor ID {vendor_id}: {total_debited_points}")

    reports=[
        {
            "balance":abs(total_points) if total_points else 0, 
            "credited":abs(total_credited_points) if total_credited_points else 0,
            "debited":total_debited_points if total_debited_points else 0
        }
    ]

    logger.info("Successfully processed all points request.")
    return RestResponse(data=reports)

@router.post("/claim/request")
def request_claim(response: Response,request1:Request, request: ClaimRequest, session=session, auth_user=auth_user):  
    request_info=f"{request1.method}:{request1.url.path} user:{auth_user['user_id']}"
    user_ip=request1.client.host
    logger.info(f"Vendor claim request - Request:{request_info},Vendor:{request},IP:{user_ip}")  
    if not auth_user.get("is_vendor"):
        response.status_code = 403
        logger.error(f"Unauthorized claim request - Request -Request:{request_info},User:{auth_user.get('email')},IP:{user_ip},Reason:Only vendor can request claims")
        return RestResponse(error="Only vendors can request claims")
    
    vendor_exists = session.exec(select(Vendor).where(Vendor.user_id == auth_user.get("user_id"))).first()
    if not vendor_exists:
        response.status_code = 400
        logger.error(f"Claim request failed -Request:{request_info}, IP:{user_ip},Reason:Vendor ID does not exist")
        return RestResponse(error="Vendor ID does not exist")

    total_points = session.exec(
        select(func.sum(Transaction.points)).where(Transaction.vendor_id == vendor_exists.id)
    ).first() or 0  

    pending_points = session.exec(
        select(func.sum(Claim.points)).where(Claim.vendor_id == vendor_exists.id, Claim.status == "PENDING")
    ).first() or 0 

    usable_points = (-1 * total_points) - pending_points

    if request.points <= 0:
        response.status_code = 400
        logger.error(f"Claim request failed -Request:{request_info}, IP:{user_ip} Reason:Points must be greater than 0")
        return RestResponse(error="Points must be greater than 0.")

    if request.points > usable_points:
        response.status_code = 400
        logger.error(f"Claim request failed - Reason {request_info},IP:{user_ip},Reason:Insufficient points or due to pending claims")
        return RestResponse(error=f"Your total available points: {-1*(total_points)}.Maximum claimable points:{usable_points}. Due to pending claim points:{pending_points}")
    claim = Claim(
        vendor_id=vendor_exists.id,
        points=request.points
    )
    session.add(claim)

    points_redeemed_by_employees = session.exec(
        select(func.sum(Transaction.points)).where(Transaction.points < 0, Transaction.vendor_id.is_not(None))
    ).first()

    if points_redeemed_by_employees is None:
        points_redeemed_by_employees =0
    else:
        points_redeemed_by_employees = abs(points_redeemed_by_employees)
    
    vendor_balance_points=session.exec(
        select(func.sum(Transaction.points)).where(Transaction.vendor_id.is_not(None))
    ).first() or 0

    points_redeemed_by_vendor = session.exec(
        select(func.sum(Transaction.points)).where(Transaction.user_id.is_(None))
    ).first() or 0

    report_entry = DailyReports(
        points_redeemed_by_employees=points_redeemed_by_employees,
        vendor_balance_points=vendor_balance_points,
        points_redeemed_by_vendor=points_redeemed_by_vendor
    )
    session.add(report_entry) 

    session.commit()
    session.refresh(claim)
    session.refresh(report_entry)
    response.status_code=201
    logger.info(f"Claim request successful - Request:{request_info},Vendor:{vendor_exists.vendor_name},Points:{claim.points},IP:{user_ip}")
    return RestResponse(data={
        "vendor_id": claim.vendor_id,
        "vendor_name": vendor_exists.vendor_name,
        "points": claim.points,
        "status": claim.status,
        "created_at": claim.created_at,
        "updated_at": claim.updated_at
    })

@router.get("/claim/requests")
def get_claims_requests_by_vendor(
    request:Request,
    response: Response,
    status: str = Query(None, description="Filter by status (approved, rejected, pending)"),
    session=session,
    auth_user=auth_user
):
    request_info=f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip=request.client.host
    logger.info(f"Fetching claim requests - Request:{request_info},IP:{user_ip}")
    if not auth_user.get("is_vendor"):
        response.status_code = 403
        logger.error(f"Unauthorized claim get request - Request:{request_info},User:{auth_user.get('email')}, IP:{user_ip}, Reason:Only vendors can request claims")
        return RestResponse(error="Only vendors can request claims.")
    vendor_id = session.exec(select(Vendor.id).where(Vendor.user_id == auth_user.get("user_id"))).first()
 
    if not vendor_id:
        response.status_code = 400
        logger.error(f"Claim request fetch failed - Request:{request_info},IP:{user_ip},Reason:Vendor details not found")
        return RestResponse(error="Vendor details not found.")
   
    vendor_details = session.exec(select(Claim).where(Claim.vendor_id == vendor_id)
                                  .order_by(Claim.created_at.desc())).all()
    if status:
        vendor_details = session.exec(select(Claim).where(Claim.vendor_id == vendor_id, Claim.status == status).
                                      order_by(Claim.created_at.desc())).all()
    logger.info(f"Claim requests fetched successfully - Request:{request_info},IP:{user_ip},Status:{status if status else 'All'}")
    
    data = [
        {
            "date": vendor_detail.created_at,
            "points": vendor_detail.points,
            "status": vendor_detail.status
        }
        for vendor_detail in vendor_details
    ]
 
    return RestResponse(data=data)

@router.put("/admin/approve/{claim_id}")
def approve_claim(response: Response, request:Request,
                  claim_id: str,claim_data:ClaimUpdate, session=session,auth_user=auth_user):
    request_info=f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip=request.client.host
    approved_points=claim_data.approved_points
    logger.info(f"Approving claim - Request:{request_info}, IP:{user_ip},Claim ID:{claim_id}, Approved points:{approved_points}")
    if not auth_user.get("is_admin"):
        response.status_code = 401
        logger.error(f"Unauthorized claim approval attempt - Request:{request_info}, IP:{user_ip},Reason:User is not an admin")
        return RestResponse(error="You are not authorized to approve claims")
    admin_name=session.exec(select(User.name).where(User.id==auth_user.get('user_id'))).first()
    claim = session.exec(select(Claim).where(Claim.id == claim_id)).first()
    if not claim:
        response.status_code = 400
        logger.error(f"Claim approval failed - Request:{request_info}, IP:{user_ip},Reason:Claim not found")
        return RestResponse(error="Claim not found")

    vendor = session.exec(select(Vendor).where(Vendor.id == claim.vendor_id)).first()
    if not vendor:
        response.status_code = 400
        logger.error(f"Claim approval failed - Request:{request_info}, IP:{user_ip}, Reason:vendor does not exist")
        return RestResponse(error="Vendor does not exist")

    if approved_points <= 0 or approved_points > claim.points:
        response.status_code = 400
        logger.error(f"Claim approval failed - Request:{request_info}, IP:{user_ip},Reason:Invalid approved points ({approved_points})")
        return RestResponse(error="Approved points must be between 1 and the requested amount")

    claim.status = "APPROVED"
    claim.points = approved_points
    claim.admin_name=admin_name
    claim.transaction_reference_id=claim_data.transaction_reference_id
    claim.updated_at = datetime.utcnow()
    session.add(claim)

    vendor_transaction = Transaction(
        id=str(uuid.uuid4()),
        vendor_id=vendor.id,
        points=approved_points,
    )
    session.add(vendor_transaction)

    session.commit()
    logger.info(f"Claim approved successfully - Request:{request_info}, IP:{user_ip}, Claim ID:{claim_id}, Approved points:{approved_points}")
    return RestResponse(
        data={"approved_points": approved_points, "updated_at": claim.updated_at},
        message=f"Claim approved successfully with {approved_points} points"
    )
 
@router.put("/admin/reject/{claim_id}")
def reject_claim(response: Response,request:Request, claim_id: str,session=session,auth_user=auth_user):
    request_info=f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip=request.client.host
    logger.info(f"Rejecting claim - Request:{request_info}, IP:{user_ip}, Claim ID:{claim_id}")
    if not auth_user.get("is_admin"):
        response.status_code = 400
        logger.error(f"Unauthorized claim rejection attemp - Request:{request_info}, IP:{user_ip}, Reason: User is not an admin")
        return RestResponse(error="You are not authorized to reject claims")
 
    claim = session.exec(select(Claim).where(Claim.id == claim_id.strip())).first()
    if not claim:
        response.status_code = 400
        logger.error(f"Claim rejection failed - Request:{request_info}, IP:{user_ip}, Reason:Claim not found")
        return RestResponse(error="Claim not found")
 
    claim.status = "REJECTED"
    claim.updated_at = datetime.utcnow()
    session.add(claim)
    session.commit()
    logger.info(f"Claim rejected successfully - Request:{request_info}, IP:{user_ip}, Claim ID:{claim_id}")
 
    return RestResponse(
        data={"updated_at": claim.updated_at},
        message="Claim rejected successfully"
    )

# Admin retrieves claim requests
@router.get("/claims/by/admin")
def get_all_claims_admin(
    request:Request,
    response: Response,
    session=session,
    auth_user=auth_user,
    status: Optional[str] = Query(None, description="Filter claims by status"),
    vendor_name: Optional[str] = Query(None, description="Filter claims by vendor name")
):
    request_info=f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip=request.client.host
    if not auth_user.get("is_admin"):
        response.status_code = 403
        logger.error(f"Unauthorized access - Request:{request_info}, User:{auth_user.get('email')}, IP:{user_ip}, Reason: Only admin can see the claim requests")
        return RestResponse(error="Only admin can see the claim requests")
    logger.info(f"Fetching all claims - Request:{request_info}, IP:{user_ip}, Filters- Status:{status}, Vendor:{vendor_name}")

    query = select(Claim, Vendor.vendor_name).join(Vendor, Claim.vendor_id == Vendor.id)

    if status:
        query = query.where(Claim.status == status)
    if vendor_name:
        query = query.where(Vendor.vendor_name == vendor_name)
    query=query.order_by(Claim.created_at.desc())
    results = session.exec(query).all()
    logger.info(f"Claims fetched successfully - Request: {request_info}, IP:{user_ip}, Total Claims:{len(results)}")

    claim_list = [
        {
            "id": str(claim.id),
            "vendor_id": str(claim.vendor_id),
            "vendor_name": vendor_name,
            "points": claim.points,
            "status": claim.status,
            "created_at": claim.created_at.isoformat(),
            "updated_at": claim.updated_at.isoformat() if claim.updated_at else None
        }
        for claim, vendor_name in results
    ]
    
    return RestResponse(data=claim_list)

 
@router.get("/claim/points")
def get_vendor_remaining_points(request:Request,response: Response, session=session, auth_user=auth_user):
    request_info=f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip=request.client.host
    logger.info(f"Fetching vendor remaining points - Request:{request_info}, IP:{user_ip}")
    if not auth_user.get("is_vendor"):
        response.status_code = 403
        logger.error(f"Unauthorized claim get request - Request:{request_info},User:{auth_user.get('email')}, IP:{user_ip}, Reason:Only vendors can retrieve requested claims")
        return RestResponse(error="Only vendors can get requested claims.")
    vendor = session.exec(select(Vendor).where(Vendor.user_id == auth_user.get("user_id"))).first()
    
    if not vendor:
        response.status_code = 400
        logger.error(f"Fetching vendor points failed - Request:{request_info}, IP:{user_ip}, Reason: Vendor ID does not exist")
        return RestResponse(error="Vendor ID does not exist")
    
    total_points = session.exec(
        select(func.sum(Transaction.points)).where(Transaction.vendor_id == vendor.id)
    ).first() or 0  

    pending_points = session.exec(
        select(func.sum(Claim.points)).where(Claim.vendor_id == vendor.id, Claim.status == "PENDING")
    ).first() or 0 

    usable_points = (-1 * total_points) - pending_points
    logger.info(f"Vendor points fetched successfull - Request:{request_info}, IP:{user_ip}, Vendor:{vendor.vendor_name}, Total Points:{-1*total_points}, Pending points:{pending_points}, Usable Points:{usable_points}")

    return RestResponse(data={
        "vendor_id": vendor.id,
        "vendor_name": vendor.vendor_name,
        "total_points": -1 * total_points,
        "pending_points": pending_points,
        "usable_points": usable_points
    })

@router.get("/reports")
def get_daily_reports(request: Request,response:Response, session=session,auth_user=auth_user):
    request_info=f"{request.method}:{request.url.path} user:{auth_user['user_id']}"
    user_ip=request.client.host
    logger.info(f"Fetching daily reports - Request:{request_info}, IP:{user_ip}")
    if not auth_user.get("is_admin"):
        logger.error(f"Unauthorized access attempt - Request:{request_info},User:{auth_user.get('email')}, IP:{user_ip}, Reason:Only admin can access reports")
        response.status_code = 403
        return RestResponse(error="Only admin can see the reports")
    reports = session.exec(select(DailyReports)).all()

    if not reports:
        logger.error(f"No reports found - Request:{request_info}, IP:{user_ip}, Reason: No daily reports found.")
        response.status_code = 404
        return RestResponse(error="No daily reports found.")
    logger.info(f"Daily reports fetched successfully - Request:{request_info}, IP:{user_ip},Reports Count:{len(reports)}")
    return RestResponse(data=[
        {
            "id": report.id,
            "date": report.created_at,  
            "points_redeemed_by_employees": report.points_redeemed_by_employees,
            "vendor_balance_points": abs(report.vendor_balance_points),
            "points_redeemed_by_vendor": report.points_redeemed_by_vendor
        }
        for report in reports
    ])