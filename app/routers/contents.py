from datetime import datetime
from uuid import uuid4
import secrets

from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File, Query

from fastapi_cache.decorator import cache

import models
from schemas import ContentCreate, User, ContentResponseWithCommentsAndLike
from database import get_db
from sqlalchemy.orm import Session
from jwt import get_current_user

router = APIRouter(tags=['contents'])


@router.post('/contents', status_code=status.HTTP_201_CREATED)
async def upload_content(title: str, file: UploadFile = File(...),
                         db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    user_id = current_user.dict().get('id_user')
    filename = file.filename
    FILEPATH = './static/images/'
    FILENAME = secrets.token_hex(5) + filename
    with open(FILEPATH + FILENAME, "wb") as buffer:
        data = await file.read()
        buffer.write(data)
    new_content = models.Content(title=title, date_time_uploaded=datetime.now(), file=FILENAME,
                                 user_id=user_id)
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    return new_content


@router.get('/contents', status_code=status.HTTP_200_OK, response_model=list[ContentResponseWithCommentsAndLike])
@cache(60)
def get_contents(search: str = Query(default=None), skip: int = Query(default=0), limit: int = Query(default=100),
                 db: Session = Depends(get_db)):
    if search is None:
        contents = db.query(models.Content).offset(skip).limit(limit).all()
    else:
        contents = db.query(models.Content).filter(models.Content.title.like(f'%{search}%')).offset(skip).limit(
            limit).all()
    return contents


@router.get('/content/{id_content}', status_code=status.HTTP_200_OK, response_model=ContentResponseWithCommentsAndLike)
def get_content(id_content: int, db: Session = Depends(get_db)):
    content = db.query(models.Content).filter(models.Content.id == id_content).first()
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    return content
