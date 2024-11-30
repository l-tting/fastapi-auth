
import database
import os
from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError


SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
ALGORITHM ='HS256'


def create_access_token(data:dict,expires_delta:timedelta | None = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expires = datetime.now(timezone.utc) + expires_delta
        else:
            expires = datetime.now(timezone.utc) + timedelta(minutes=10)
        to_encode.update({"exp":expires})

        encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    except Exception as error:
        return {"Error creating access token":error}
    return encoded_jwt

def create_refresh_token(data:dict,expires_delta:timedelta | None = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expires = datetime.now(timezone.utc) + expires_delta
        else:
            expires = datetime.now(timezone.utc) + timedelta(days=2)
        to_encode.update({"exp":expires})
        encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    except Exception as error:
        return {"Error creating refresh token":error}
    return encoded_jwt
