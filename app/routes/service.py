from fastapi import APIRouter, status, HTTPException, Depends,  Form, File, UploadFile
from app.database import SessionLocale
from sqlalchemy.orm import Session
from typing import Annotated, List, Optional
from app.models.vehicle import Vehicle
from app.models.user import User
from app.schemas.vehicle import VehicleResponse, VehicleCreate
from app.service.user import decode_access_token
from app.schemas.service import ServiceSchema
import os
import shutil
router = APIRouter(prefix="/api/service", tags=["Service API"])

UPLOAD_DIRECTORY = "uploads/"


def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()


db_depandancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(decode_access_token)]


@app.post("/service/book/")
def book_service(service: ServiceSchema, db: db_depandancy)):
    db_service= models.Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service
