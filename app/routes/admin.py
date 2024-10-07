from fastapi import APIRouter, status, HTTPException, Depends, File, UploadFile, Form
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.admin import Admin

from app.database import SessionLocale
from sqlalchemy.orm import Session
from typing import Annotated, List
from app.service.user import create_accesss_token, decode_access_token, hash_pass
from app.schemas.user import UserResponse
from app.schemas.admin import AdminCreate


def get_db():
    db = SessionLocale()
    try:
        yield db
    finally:
        db.close()


db_depandancy = Annotated[Session, Depends(get_db)]
user_dependancy = Annotated[dict, Depends(decode_access_token)]

router = APIRouter(prefix="/api/admin", tags=["Admin API"])


@router.post('/create-admin', status_code=status.HTTP_201_CREATED)
async def create_admin(adminresponse: AdminCreate, db: db_depandancy):
    admin = Admin(
        name=adminresponse.name,
        email=adminresponse.email,
        password=hash_pass(adminresponse.password),
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)


@router.get('/get-customers', response_model=List[UserResponse])
async def get_user(user: user_dependancy, db: db_depandancy):
    if user:
        admin = db.query(Admin).filter(
            Admin.id == user.get("user_id")).first()
        if admin:
            user = db.query(User).all()
            return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials")
