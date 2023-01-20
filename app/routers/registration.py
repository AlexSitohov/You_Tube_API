from fastapi import APIRouter, status, Depends
from schemas import User
from database import get_db
from sqlalchemy.orm import Session
from hash import hash
import models

router = APIRouter(tags=['registration'])


@router.post('/registration', status_code=status.HTTP_201_CREATED)
def registration(user: User, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
