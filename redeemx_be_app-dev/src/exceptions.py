from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, OperationalError, DatabaseError, DataError, ProgrammingError
from pydantic import ValidationError
from starlette.responses import JSONResponse
import re

from src.logging_config import logger



async def request_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    error_details = [{"field": err["loc"], "error": err["msg"]} for err in errors]
    logger.error(f"RequestValidationError: {error_details}, {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=400,
        content={
            "data": None,
            "message": "",
            "error": [
                f"{(err['loc'][1] + ' ') if len(err['loc']) > 1 else ''}{err['msg'][6:].split(',', 1)[-1].strip()}"
                for err in errors
            ]
        }
    )


async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"data": None, "message": "", "error": "An unexpected error occurred."}
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=exc.status_code,
        content={"data": None, "message": "", "error": str(exc.detail)}
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    error_message = str(exc.orig)
    logger.error(f"Integrity Error: {error_message}", exc_info=True)

    if "duplicate key value violates unique constraint" or "Duplicate entry" in error_message:
        return JSONResponse(
            status_code=400,
            content={"data": None, "message": "", "error": "This value already exists."}
        )

    elif "a foreign key constraint fails" in error_message:
        return JSONResponse(
            status_code=422,
            content={"data": None, "message": "", "error": "Foreign key constraint violation."}
        )

    return JSONResponse(
        status_code=400,
        content={"data": None, "message": "", "error": "Database integrity error occurred."}
    )

async def operational_error_handler(request: Request, exc: OperationalError):
    error_message = str(exc.orig)
    logger.error(f"Operational Error: {error_message}", exc_info=True)

    # Extract the missing column name using regex
    column_match = re.search(r"Unknown column '(.+?)'", error_message)
    column_name = column_match.group(1) if column_match else "unknown column"

    return JSONResponse(
        status_code=400,
        content={
            "data": None,
            "message": "",
            "error": f"The column '{column_name}' does not exist in the database. Please check your schema and try again."
        }
    )


async def database_error_handler(request: Request, exc: DatabaseError):
    logger.error(f"Database Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"data": None, "message": "", "error": "A database error occurred."}
    )


async def data_error_handler(request: Request, exc: DataError):
    error_message = str(exc.orig)
    logger.error(f"Data Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=400,
        content={
            "data": None,
            "message": "",
            "error": f"Please enter a valid data"
        }
    )


async def programming_error_handler(request: Request, exc: ProgrammingError):
    logger.error(f"SQL Syntax Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"data": None, "message": "", "error": "A database programming error occurred."}
    )


async def pydantic_validation_error_handler(request: Request, exc: ValidationError):
    logger.error(f"Pydantic Validation Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=422,
        content={"data": None, "message": "", "error": "Invalid input data."}
    )


async def permission_error_handler(request: Request, exc: PermissionError):
    logger.error(f"Permission Denied: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=403,
        content={"data": None, "message": "", "error": "You do not have permission to perform this action."}
    )


async def connection_error_handler(request: Request, exc: ConnectionError):
    logger.error(f"Connection Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=503,
        content={"data": None, "message": "", "error": "Service unavailable. Please check your connection."}
    )


async def timeout_error_handler(request: Request, exc: TimeoutError):
    logger.error(f"Timeout Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=504,
        content={"data": None, "message": "", "error": "Request timed out. Please try again later."}
    )


async def file_not_found_error_handler(request: Request, exc: FileNotFoundError):
    logger.error(f"File Not Found: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=404,
        content={"data": None, "message": "", "error": "The requested file was not found."}
    )


async def memory_error_handler(request: Request, exc: MemoryError):
    logger.error(f"Memory Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"data": None, "message": "", "error": "Server ran out of memory."}
    )


async def recursion_error_handler(request: Request, exc: RecursionError):
    logger.error(f"Recursion Error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"data": None, "message": "", "error": "Too many recursive calls detected."}
    )

