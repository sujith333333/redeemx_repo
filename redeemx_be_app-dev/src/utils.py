#Api for adding user using excel data
from fastapi import  UploadFile, HTTPException, APIRouter
import pandas as pd
from src.database import session
from src.user.utils import generate_password
from src.user.models import User

router = APIRouter()

@router.post("/user/data/upload-excel/")
async def upload_excel(file: UploadFile, session=session):

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are allowed.")

    try:
        df = pd.read_csv(file.file)
        for index, row in df.iterrows():
            emp_id = str(row["Emp ID"]) if str(row["Emp ID"]) else "NA"
            username = str(row["Emp ID"]) if str(row["Emp ID"]) else "NA"
            name = row["Name"] if row["Name"] else "NA"
            mobile_number = int(row["Official Mobile Number"]) if int(row["Official Mobile Number"]) else 9999999999
            email = row["Email"]
            hash_password = generate_password(name, emp_id)

            user = User(
                emp_id=emp_id,
                name=name,
                mobile_number=str(mobile_number),
                email=email,
                password=hash_password,
                is_user = True,
                username = username
            )
         
            session.add(user)
        session.commit()

        return {"message": "Excel data successfully loaded into the database."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
