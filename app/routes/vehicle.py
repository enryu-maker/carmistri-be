from fastapi import APIRouter, status, HTTPException, Depends,  Form, File, UploadFile
from app.database import SessionLocale
from sqlalchemy.orm import Session
from typing import Annotated, List, Optional
from app.models.vehicle import Vehicle
from app.models.user import User
from app.schemas.vehicle import VehicleResponse, VehicleCreate
from app.service.user import decode_access_token
import os
import shutil
router = APIRouter(prefix="/api/vehicle", tags=["Vehicle API"])

UPLOAD_DIRECTORY = "uploads/"


def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()


db_depandancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(decode_access_token)]


@router.post("/create-vehicle/", response_model=VehicleResponse)
async def create_vehicle(
    user: user_dependancy,
    db: db_depandancy,
    make: str = Form(...),
    model: str = Form(...),
    number: str = Form(...),
    icon: Optional[UploadFile] = File(None),  # Optional file upload for icon

):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")

    # Check if user exists
    db_user = db.query(User).filter(User.id == user.get("user_id")).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Handle file upload for the icon
    file_path = None
    if icon:
        if not os.path.exists(UPLOAD_DIRECTORY):
            os.makedirs(UPLOAD_DIRECTORY)  # Create directory if not exists
        file_location = f"{UPLOAD_DIRECTORY}{icon.filename}"

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(icon.file, buffer)
        file_path = file_location

    # Create new vehicle with uploaded icon path (if file uploaded)
    db_vehicle = Vehicle(
        make=make,
        model=model,
        number=number,
        icon=file_path,  # Save file path to the database
        user_id=db_user.id
    )

    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)

    return db_vehicle
