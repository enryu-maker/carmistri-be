import random
import string
import datetime
from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from jose import jwt, JWTError
import requests
from typing import Annotated
from passlib.context import CryptContext
load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='/api/user/verify-user')

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_pass(password: str):
    return bcrypt_context.hash(password)


def generate_otp():
    return ''.join(random.choices(string.digits, k=4))


def send_otp(mobile_number: str) -> bool:

    url = "https://auth.otpless.app/auth/v1/initiate/otp"
    print(url)
    payload = {
        "phoneNumber": "+91" + mobile_number,
        "expiry": 30,
        "otpLength": 4,
        "channels": ["WHATSAPP", "SMS"],
    }
    headers = {
        "clientId": "1FFE873E69F211EFAC7102E825E2EA5C",
        "clientSecret": "ac7102e825e2ea5c1ffe877769f211ef",
        "Content-Type": "application/json"
    }

    response = requests.request(
        "GET", url,
        headers=headers, data=payload)
    print(response)
    if response.status_code == 200:
        return {
            "status": True,
            "message": "OTP sent successfully"
        }
    return {
        "status": False,
        "message": "Error sending OTP"
    }


def verify_otp(otp: str, request_id: str) -> bool:

    url = "https://auth.otpless.app/auth/v1/verify/otp"
    print(url)
    payload = {
        "requestId": request_id,
        "otp": otp
    }
    headers = {
        "clientId": "<api-key>",
        "clientSecret": "<api-key>",
        "Content-Type": "application/json"
    }

    response = requests.request(
        "GET", url,
        headers=headers, data=payload)
    if response.status_code == 200:
        return True
    return False


def create_accesss_token(username: str, user_id: int, expiry: timedelta):
    encode = {
        'sub':  username,
        'id': user_id
    }
    expires = datetime.datetime.utcnow() + expiry
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get('sub')
        user_id: int = payload.get('id')
        if name is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid access token")
        return {
            'name': name,
            'user_id': user_id
        }
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
