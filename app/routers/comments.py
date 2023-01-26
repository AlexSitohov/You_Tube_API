from fastapi import APIRouter, status, Depends, HTTPException

import models
from schemas import User, Comment
from database import get_db
from sqlalchemy.orm import Session
from jwt import get_current_user

router = APIRouter(tags=['comments'])


@router.post('/comments', status_code=status.HTTP_200_OK)
def comment(comment_data: Comment, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        comment_new = models.Comment(**comment_data.dict(), user_id=current_user.dict().get('id_user'))
        db.add(comment_new)
        db.commit()
        db.refresh(comment_new)
        return comment_new
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'content with id: {comment_data.content_id} not found ')


@router.get('/my-comments')
def get_my_comments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    my_comments = db.query(models.Comment).filter(models.Comment.user_id == current_user.dict().get('id_user')).all()
    return my_comments
