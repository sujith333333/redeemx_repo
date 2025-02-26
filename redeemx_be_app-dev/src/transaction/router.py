from fastapi import APIRouter, Response, Query, UploadFile, File, Request
from sqlmodel import select, or_, func,case
from datetime import datetime

import pandas as pd
import calendar


from src.response import RestResponse
from src.database import session
from src.user.models import User
from src.vendor.models import Vendor
from src.transaction.models import Transaction
from src.auth.dependencies import auth_user
from src.transaction.schemas import TransactionUserInputSchema
from src.logging_config import logger

router = APIRouter()


#User transactions
@router.post("/admin/user/transaction")
def admin_user_transaction(request:Request, transaction:Transaction, response:Response, session=session, auth_user=auth_user):
    user_ip = request.client.host
    if auth_user.get("is_admin"):
        request_info = f"{request.method}:{request.url.path} user:{auth_user.get('user_id', 'Unknown')}"
        
        logger.info(f"Admin user transaction - Incoming request:{request_info}, IP: {user_ip}")
        
        logger.info(f"Processing transaction - User ID: {transaction.user_id}, Points: {transaction.points}, Vendor: {transaction.vendor_id}")
        
        logger.debug(f"Adding transaction for user {transaction.user_id} to database session")
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        response.status_code = 201
        logger.info(f"Points added successfully for user ID {transaction.user_id}, Transaction ID: {transaction.id}")
        return RestResponse(data=transaction, message="Points added successfully")
    logger.error(f"Unauthorized access attempt by user {auth_user.get('user_id', 'Unknown')} from IP {user_ip}")
    return RestResponse(error="Your not authorized")


@router.post("/user/vendor/transaction")
def user_vendor_transaction(request:Request, transaction:TransactionUserInputSchema, response:Response, session=session, auth_user=auth_user):
    user_id = auth_user.get("user_id", "Unknown")
    if auth_user.get("is_user"):
        #check for the vendor
        request_info = f"{request.method}:{request.url.path},User ID: {user_id}, Vendor Name: {transaction.vendor_name}, Vendor ID: {transaction.vendor_id}, Points: {transaction.points}"
        logger.info(f"Incoming request for user-vendor transaction: {request_info}")

        get_vendor = session.exec(select(Vendor).where(or_(Vendor.vendor_name == transaction.vendor_name, 
                                                           Vendor.user_id == transaction.vendor_id))).first()
        if not get_vendor:
            response.status_code = 400
            logger.error(f"Vendor not found for transaction request: {request_info}")
            return RestResponse(error="No vendor details found")
        
        user_points = session.exec(select(func.sum(Transaction.points)).where(Transaction.user_id == auth_user.get("user_id"))).first()
        if not user_points:
            response.status_code = 400
            logger.error(f"User ID {user_id} has no points available.")
            return RestResponse(error="You don't have a points")
        
        if user_points < transaction.points:
            response.status_code = 400
            logger.error(f"User ID {user_id} tried to transfer {transaction.points} points but only has {user_points} points.")
            return RestResponse(error="You don't have a enough points")
        
        if transaction.points <= 0:
            response.status_code = 400
            return RestResponse(error="Points should be greater than zero")
        
        transaction_db = Transaction(
            user_id=auth_user.get("user_id"),
            vendor_id=get_vendor.id,
            points=-1*(transaction.points)
        )
        session.add(transaction_db)
        session.commit()
        session.refresh(transaction_db)
        response.status_code = 201
        logger.info(f"User ID {user_id} transferred {transaction.points} points to Vendor ID {get_vendor.id}.")
        return RestResponse(data=transaction, message="Points transfered successfully")
    logger.error(f"Unauthorized access attempt by user: {auth_user}")
    return RestResponse(error="Your not authorized")


@router.get("/user/points")
def user_get_points(response:Response, session=session, auth_user=auth_user):
    user_points = session.exec(select(func.sum(Transaction.points)).where(Transaction.user_id == auth_user.get("user_id"))).first()
    points = user_points if user_points else 0
    return RestResponse(data={"points":points})


#Vendor Transactions
@router.get("/vendor/points")
def vender_get_points(response:Response, session=session, auth_user=auth_user):
    vendor_id = session.exec(select(Vendor.id).where(Vendor.user_id == auth_user.get("user_id"))).first()
    user_points = session.exec(select(func.sum(Transaction.points)).where(Transaction.vendor_id == vendor_id)).first()
    points = user_points if user_points else 0
    return RestResponse(data={"points":-1*points})



@router.post("/vendor/transaction/admin")
def vendor_transaction_admin(transaction:Transaction, response:Response, session=session, auth_user=auth_user):
    if auth_user.get("is_admin"):
        get_vendor = session.exec(select(Vendor).where(or_(Vendor.id == transaction.vendor_id, 
                                                           Vendor.user_id == transaction.vendor_id))).first()
    
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        response.status_code = 201
        logger.info(f"Points added successfully for user ID {transaction.user_id}")
        return RestResponse(data=transaction, message="Points transfered successfully")
    logger.error(f"Unauthorized access attempt by user: {auth_user}")
    return RestResponse(error="Your not authorized")


@router.post("/user-data/upload/transaction")
async def upload_file(
    request: Request, response: Response, file: UploadFile = File(...), session=session, auth_user=auth_user
):
    user_id = auth_user.get("user_id", "Unknown")
    if auth_user.get("is_admin"):
        
        request_info = f"{request.method}:{request.url.path}, User ID: {user_id}"
        logger.info(f"Incoming request for assigned points: {request_info}")

        if not file.filename.endswith((".csv", ".xlsx")):
            response.status_code = 400
            logger.error(f"Invalid file format attempted: {file.filename}")
            return RestResponse(error="Invalid file format. Please upload a CSV or Excel file.")

        if file.filename.endswith(".csv"):
            df = pd.read_csv(file.file)
        else:
            df = pd.read_excel(file.file)

        user_list = session.exec(select(User).filter(User.is_user == True)).all()
        excel_emp_ids = df["E. Code"].unique().tolist()

        unassigned_data = []
        transactions_added = 0
        transaction_user_id = None

        for user in user_list:
            if user.emp_id in excel_emp_ids:
                transaction = Transaction(user_id=user.id, points=20)
                session.add(transaction)
                transactions_added += 1
                transaction_user_id = user.id
            else:
                unassigned_data.append({"emp_id": user.emp_id, "details": "User not registered"})

        session.commit()
        
        logger.info(f"File '{file.filename}' processed successfully. Transactions added: {transactions_added}")
        
        if transaction_user_id:
            logger.info(f"File processed successfully for user ID {transaction_user_id}")

        if unassigned_data:
            logger.warning(f"Unassigned users from file '{file.filename}': {unassigned_data}")

        return RestResponse(data=unassigned_data, message="File processed successfully.")

    
    user_id = auth_user.get("user_id", "Unknown")
    response.status_code = 400
    logger.error(f"Unauthorized access attempt by user: {auth_user}, User ID: {user_id}")
    return RestResponse(error="You are not authorized")



#admin weekly points
@router.get("/overallpoints")
def get_overall_points(response:Response,request:Request,
    start_date: datetime = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: datetime = Query(None, description="End date in YYYY-MM-DD format"),
    session = session, auth_user=auth_user):

    user_id = auth_user.get("user_id", "Unknown")
    if auth_user.get("is_admin"):
        
        request_info = f"{request.method}:{request.url.path},User ID: {user_id} "
        logger.info(f"Incoming request for overall points: {request_info}")

        first_transaction_date = session.exec(select(func.min(Transaction.created_at))).first()
        today=datetime.today()
        
        if start_date is None:
            start_date = first_transaction_date
        if end_date is None:
            end_date=today
            
        if start_date > end_date:
            response.status_code = 400
            logger.error(f"Invalid date range: Start date {start_date} is after End date {end_date}")
            return RestResponse(error="Start date cannot be after end date.")
    
        logger.info(f"Fetching overall points from {start_date} to {end_date}")
        stmt = select(
                func.coalesce(
                    func.sum(case((Transaction.vendor_id.is_(None), Transaction.points), else_=0)),0
                                ).label("points_assigned_to_employee"),
                func.coalesce(
                    func.sum(case((Transaction.user_id.isnot(None), Transaction.points), else_=0)),0
                                ).label("points_assigned_to_employee_balance"),
                func.coalesce(func.abs(
                func.sum(case(((Transaction.vendor_id.isnot(None)) & (Transaction.user_id.isnot(None)),
                                Transaction.points), else_=0))), 0).label("total_points_user_sends_to_vendor"),

                func.coalesce((func.sum(case((Transaction.user_id.is_(None),Transaction.points), else_=0))), 0
                ).label("points_claimed_by_vendor"),)
        
        if start_date and end_date:
            stmt = stmt.where(Transaction.created_at.between(start_date, end_date))
         

        result = session.exec(stmt).first()  
        
        points_yet_to_approve_to_vendor=abs(result.total_points_user_sends_to_vendor-result.points_claimed_by_vendor)
        
        logger.info(f"Query executed successfully. Data retrieved: {result}")
        return RestResponse(data = {
            "points_assigned_to_employee": result.points_assigned_to_employee,
            "points_assigned_to_employee_balance": result.points_assigned_to_employee_balance,
            "total_points_user_sends_to_vendor": result.total_points_user_sends_to_vendor,
            "points_claimed_by_vendor": result.points_claimed_by_vendor,
            "points_yet_to_approve_to_vendor": points_yet_to_approve_to_vendor,
        })
    response.status_code =400
    logger.error(f"Unauthorized access attempt by user: {auth_user},User ID: {user_id}")
    return RestResponse(error="You are not authorized")


#admin monthly points
@router.get("/monthlypoints")
def get_monthly_points(response:Response,request:Request,
    start_date: datetime = Query(None, description="Start date in YYYY-MM-DD format"),
    end_date: datetime = Query(None, description="End date in YYYY-MM-DD format"),
    month: int = Query(None, description="Month number (1-12)"),
    year: int =Query(None, description="Year (e.g., 2024)"),
    session = session, auth_user=auth_user):

    user_id = auth_user.get("user_id", "Unknown")
    if auth_user.get("is_admin"):
        
        request_info = f"{request.method}:{request.url.path},User ID: {user_id} "
        logger.info(f"Incoming request for monthly points: {request_info}")

        if start_date is None and end_date is None and month is None and year is None:
            start_date, end_date = None, None 

        elif month is not None and year is not None:
            if not (1 <= month <= 12):
                response.status_code=400
                logger.error(f"Invalid month {month} received from user: {auth_user},User ID: {user_id}")
                return RestResponse(error="Invalid month. Must be between 1 and 12.")
                    
            
            first_day = datetime(year, month, 1)
            last_day = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)

            start_date = first_day
            end_date = last_day
        
        elif month is not None and year is None:
            if not (1 <= month <= 12):
                response.status_code=400
                logger.error(f"Invalid month {month} received from user: {auth_user},User ID: {user_id}")
                return RestResponse(error="Invalid month. Must be between 1 and 12.")
                    
            year = datetime.now().year 
            first_day = datetime(year, month, 1)
            last_day = datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)

            start_date = first_day
            end_date = last_day
        else: 
            if start_date is not None and end_date is not None and start_date > end_date:
                response.status_code=400
                logger.error(f"Invalid date range: {start_date} to {end_date} from user: {auth_user},User ID: {user_id}")
                return RestResponse(error="Start date cannot be after end date.")
        
        
        logger.info(f"Fetching monthly points from {start_date} to {end_date} for user: {auth_user},User ID: {user_id}")
        stmt = select(
                func.coalesce(
                    func.sum(case((Transaction.vendor_id.is_(None), Transaction.points), else_=0)),0
                                ).label("points_assigned_to_employee"),
                func.coalesce(
                    func.sum(case((Transaction.user_id.isnot(None), Transaction.points), else_=0)),0
                                ).label("points_assigned_to_employee_balance"),
                func.coalesce(func.abs(
                func.sum(case(((Transaction.vendor_id.isnot(None)) & (Transaction.user_id.isnot(None)),
                                Transaction.points), else_=0))), 0).label("total_points_user_sends_to_vendor"),

                func.coalesce((func.sum(case((Transaction.user_id.is_(None),Transaction.points), else_=0))), 0
                ).label("points_claimed_by_vendor"),)
        
        if start_date and end_date:
            stmt = stmt.where(Transaction.created_at.between(start_date, end_date))
         

        result = session.exec(stmt).first()  
        
        points_yet_to_approve_to_vendor=abs(result.total_points_user_sends_to_vendor-result.points_claimed_by_vendor)
        
        logger.info(f"Query executed successfully. Data retrieved: {result}")
        logger.info(f"Response generated successfully for user: {auth_user},User ID: {user_id}")
        return RestResponse(data = {
            "points_assigned_to_employee": result.points_assigned_to_employee,
            "points_assigned_to_employee_balance": result.points_assigned_to_employee_balance,
            "total_points_user_sends_to_vendor": result.total_points_user_sends_to_vendor,
            "points_claimed_by_vendor": result.points_claimed_by_vendor,
            "points_yet_to_approve_to_vendor": points_yet_to_approve_to_vendor,
        })
    
    response.status_code =400
    logger.error(f"Unauthorized access attempt by user: {auth_user}, User ID: {user_id}")
    return RestResponse(error="You are not authorized")