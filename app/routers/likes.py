from fastapi import APIRouter, status, Depends, HTTPException

import models
from schemas import Like, User, ContentResponseWithCommentsAndLike
from database import get_db
from sqlalchemy.orm import Session
from jwt import get_current_user
from sqlalchemy import func as generic_functions

router = APIRouter(tags=['likes'])


@router.post('/likes', status_code=status.HTTP_200_OK)
def like(like_date: Like, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    like_query = db.query(models.Like).filter(models.Like.user_id == current_user.dict().get('id_user'),
                                              models.Like.content_id == like_date.content_id)
    like = like_query.first()
    if like:
        like_query.delete()
        db.commit()
        return {'msg': 'оценка удаленна'}
    elif not like:
        new_like = models.Like(user_id=current_user.dict().get('id_user'), content_id=like_date.content_id)
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
        return {'msg': 'оценка поставлена'}


@router.get('/liked-content', status_code=status.HTTP_200_OK, response_model=list[ContentResponseWithCommentsAndLike])
def get_liked_content(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    liked_content = db.query(models.Content).join(
        models.Like, models.Like.content_id == models.Content.id).join(models.User,

                                                                       models.User.id == models.Like.user_id
                                                                       ).group_by(
        models.Content.id).filter(
        models.User.id == current_user.dict().get('id_user')).all()

    return liked_content
