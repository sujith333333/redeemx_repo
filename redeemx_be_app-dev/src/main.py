import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)


from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import uvicorn
from sqlalchemy.exc import IntegrityError, OperationalError, DatabaseError, DataError, ProgrammingError
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError


from src.database import create_db_and_tables
from src.user.router import router as user_router
from src.auth.router import router as auth_router
from src.vendor.router import router as vendor_router
from src.transaction.router import router as transaction_router
from src.utils import router as user_upload_router
from src.exceptions import (
    request_exception_handler,
    global_exception_handler,
    http_exception_handler,
    integrity_error_handler,
    operational_error_handler,
    database_error_handler,
    data_error_handler,
    programming_error_handler,
    pydantic_validation_error_handler,
    permission_error_handler,
    connection_error_handler,
    timeout_error_handler,
    file_not_found_error_handler,
    memory_error_handler,
    recursion_error_handler
)


load_dotenv()
create_db_and_tables()

app = FastAPI()


origins = [
    
    "http://localhost:3000",
    "http://3.95.158.243:3000",
    "http://3.80.60.48:3000"
]

#Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)
app.add_middleware(SessionMiddleware, secret_key="abc")


#Global Exceptions
app.add_exception_handler(RequestValidationError, request_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(OperationalError, operational_error_handler)
app.add_exception_handler(DatabaseError, database_error_handler)
app.add_exception_handler(DataError, data_error_handler)
app.add_exception_handler(ProgrammingError, programming_error_handler)
app.add_exception_handler(ValidationError, pydantic_validation_error_handler)
app.add_exception_handler(PermissionError, permission_error_handler)
app.add_exception_handler(ConnectionError, connection_error_handler)
app.add_exception_handler(TimeoutError, timeout_error_handler)
app.add_exception_handler(FileNotFoundError, file_not_found_error_handler)
app.add_exception_handler(MemoryError, memory_error_handler)
app.add_exception_handler(RecursionError, recursion_error_handler)


#Routers
app.include_router(auth_router, prefix='/api/v1/auth', tags=["Authentication"])
app.include_router(user_router, prefix='/api/v1/user', tags=["Users"])
app.include_router(vendor_router, prefix='/api/v1/vendor', tags=["Vendors"])
app.include_router(transaction_router, prefix='/api/v1/transaction', tags=["Transactions"])
app.include_router(user_upload_router, prefix='/api/v1/user-upload', tags=["User Data Dumping"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)