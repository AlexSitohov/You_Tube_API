from fastapi import APIRouter, status, Depends, HTTPException

import models
from schemas import ContentCreate, UserCreate
from database import get_db
from sqlalchemy.orm import Session
from jwt import get_current_user

router = APIRouter(tags=['contents'])


@router.post('/contents', status_code=status.HTTP_201_CREATED)
def upload_content(content: ContentCreate, db: Session = Depends(get_db),
                   current_user: UserCreate = Depends(get_current_user)):
    new_content = models.Content(**content.dict(), user_id=current_user.dict().get('id_user'))
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    return new_content


@router.get('/contents', status_code=status.HTTP_200_OK)
def get_contents(db: Session = Depends(get_db)):
    contents = db.query(models.Content).all()
    return contents
