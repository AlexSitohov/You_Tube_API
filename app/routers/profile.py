from fastapi import APIRouter, status, Depends, HTTPException

import models
from schemas import User, Profile
from database import get_db
from sqlalchemy.orm import Session
from jwt import get_current_user

router = APIRouter(tags=['profile'])


@router.get('/profile', status_code=status.HTTP_200_OK)
def get_my_profile(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    profile = db.query(models.User).filter(models.User.id == current_user.dict().get('id_user')).first()
    return profile


@router.delete('/profile-update', status_code=status.HTTP_200_OK)
def update_profile(db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    profile_query = db.query(models.User).filter(models.User.id == current_user.dict().get('id_user'))
    profile = profile_query.first()
    profile_query.delete(synchronize_session='evaluate')

    db.commit()
    return profile
