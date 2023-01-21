from fastapi import APIRouter, status, Depends, HTTPException

import models
from schemas import ContentCreate, User, ContentResponseWithCommentsAndLike
from database import get_db
from sqlalchemy.orm import Session
from jwt import get_current_user

router = APIRouter(tags=['contents'])


@router.post('/contents', status_code=status.HTTP_201_CREATED)
def upload_content(content: ContentCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    new_content = models.Content(**content.dict(), user_id=current_user.dict().get('id_user'))
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    return new_content


@router.get('/contents', status_code=status.HTTP_200_OK, response_model=list[ContentResponseWithCommentsAndLike])
def get_contents(db: Session = Depends(get_db)):
    contents = db.query(models.Content).all()
    return contents


@router.get('/content/{id_content}', status_code=status.HTTP_200_OK, response_model=ContentResponseWithCommentsAndLike)
def get_content(id_content: int, db: Session = Depends(get_db)):
    content = db.query(models.Content).filter(models.Content.id == id_content).first()
    if not content:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    return content
