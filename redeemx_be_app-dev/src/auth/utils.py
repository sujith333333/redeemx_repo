from datetime import datetime, timedelta
import os
import jwt


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt

def decode_access_token(token: str):
    payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=os.getenv("ALGORITHM"))
    return payload

    