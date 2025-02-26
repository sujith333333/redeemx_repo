from fastapi import HTTPException,APIRouter
from sqlmodel import select
import httpx

from src.user.models import User
from src.database import session
from src.transaction.models import Transaction
from src.response import RestResponse

router = APIRouter()

THIRD_PARTY_API_URL = "http://127.0.0.1:8000/employees"  

async def fetch_all_employees():
    async with httpx.AsyncClient() as client:
        response = await client.get(THIRD_PARTY_API_URL)
        if response.status_code == 404:
            return None
        return response.json()

@router.post("/process/all/transactions")
async def process_transactions(session=session):
    third_party_employees = await fetch_all_employees()
    if not third_party_employees:
        raise HTTPException(status_code=404, detail="No employees found in third-party API")
    local_employees = session.exec(select(User)).all()
    local_emp_ids = {emp["empid"] for emp in third_party_employees}
    
    unassigned_data = []
    for emp in local_employees:
        if emp.emp_id in local_emp_ids:  
            transaction = Transaction(user_id=emp.id, points=20)
            session.add(transaction)
        else:
            unassigned_data.append({"emp_id": emp.emp_id, "details": "User not registered"})
    session.commit()
    return RestResponse(data=unassigned_data, message="File processed successfully.")