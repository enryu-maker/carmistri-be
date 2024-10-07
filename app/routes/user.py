from fastapi import APIRouter, status, HTTPException, Depends, File, UploadFile, Form
from app.database import SessionLocale
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, OTPVerify, UserResponse
from app.models.user import User
from app.models.vehicle import Vehicle
from typing import Annotated, List
import os
from pathlib import Path
from dotenv import load_dotenv
from app.service.user import create_accesss_token, decode_access_token, send_otp
import shutil
import json
load_dotenv()
API_KEY = os.getenv("API_KEY")
UPLOAD_DIRECTORY = "uploads/"

router = APIRouter(prefix="/api/user", tags=["User API"])


def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()


db_depandancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(decode_access_token)]


@router.get('/get-users', response_model=List[UserResponse])
async def get_user(db: db_depandancy):
    user = db.query(User).all()
    return user


@router.get('/get-cities')
async def get_cities():
    try:
        json_file_path = Path('app/data/predefinedCities.json')

        if not json_file_path.exists():
            raise HTTPException(
                status_code=404, detail="Cities file not found")

        with open(json_file_path, 'r') as file:
            data = json.load(file)

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete-user")
async def delete_user(db: db_depandancy, id: int):
    # delete user
    try:
        # Query the database to find the record with the given id
        user_to_delete = db.query(User).filter(
            User.id == id).first()

        if user_to_delete is None:
            raise HTTPException(status_code=404, detail="Method not found")

        # Delete the record
        db.delete(user_to_delete)
        db.commit()

        return {"status": "success", "message": "User deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=f"Error deleting method: {str(e)}")


@router.get('/get-profile', response_model=UserResponse)
async def get_user(user: user_dependancy, db: db_depandancy):
    if user:
        user = db.query(User).filter(
            User.id == user.get("user_id")).first()
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")


@router.post('/create-user', status_code=status.HTTP_201_CREATED)
async def create_user(
    full_name: str = Form(...),
    email: str = Form(...),
    mobile_number: str = Form(...),
    file: UploadFile = File(None),  # Optional file upload
    db: Session = Depends(get_db)
):
    # Check if the user already exists
    db_user = db.query(User).filter(
        User.mobile_number == mobile_number).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    # File handling: Save uploaded file (if provided)
    file_path = None
    if file:
        if not os.path.exists(UPLOAD_DIRECTORY):
            # Create the directory if it doesn't exist
            os.makedirs(UPLOAD_DIRECTORY)
        file_location = f"{UPLOAD_DIRECTORY}{file.filename}"

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_path = file_location

    # Create a new user
    new_user = User(
        full_name=full_name,
        mobile_number=mobile_number,
        email=email,
        icon=file_path  # Save file path if a file was uploaded
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    try:
        otp_status = send_otp(new_user.mobile_number)
        return otp_status
    except Exception as e:

        return {"msg": e}
