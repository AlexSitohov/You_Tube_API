from fastapi import APIRouter, status, Depends, HTTPException

from database import get_db
from sqlalchemy.orm import Session
from hash import hash
import models

router = APIRouter(tags=['users'])


@router.get('/users', status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/user/{user_id}', status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    user = user_query.first()
    return user
