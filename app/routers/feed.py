from fastapi import APIRouter, Depends

import models
from schemas import User
from database import get_db
from sqlalchemy.orm import Session
from jwt import get_current_user
from sqlalchemy import func as generic_functions

router = APIRouter(tags=['feed'])


@router.get('/feed')
def get_my_feed(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    my_subscriptions_id = db.query(models.Subscription.youtuber_id).select_from(models.Subscription).join(
        models.User,
        models.User.id == models.Subscription.follower_id).group_by(
        models.Subscription.youtuber_id).filter(
        models.User.id == current_user.dict().get('id_user')).all()

    lst_of_my_subscriptions_and_me_ids = [my_subscriptions_id[i][0] for i in range(len(my_subscriptions_id))]
    lst_of_my_subscriptions_and_me_ids.append(current_user.dict().get('id_user'))
    feed = db.query(models.Content, generic_functions.count(models.Like.user_id).label("Likes")).join(models.User,
                                                                                                      models.User.id == models.Content.user_id).group_by(
        models.Content.id).join(
        models.Like, models.Like.content_id == models.Content.id, isouter=True).where(
        models.User.id.in_(lst_of_my_subscriptions_and_me_ids)).all()
    return feed
