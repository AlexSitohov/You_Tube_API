from fastapi import APIRouter, Depends, status, HTTPException

import models
from schemas import Subscription, User
from database import get_db
from sqlalchemy.orm import Session
from jwt import get_current_user

router = APIRouter(tags=['subscriptions'])


@router.post('/subscriptions', status_code=status.HTTP_201_CREATED)
def subscribe(subscription_data: Subscription, db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):
    subscription_query = db.query(models.Subscription).filter(
        models.Subscription.youtuber_id == subscription_data.youtuber_id,
        models.Subscription.follower_id == current_user.dict().get('id_user'))
    subscription = subscription_query.first()
    if subscription:
        subscription_query.delete()
        db.commit()
        return {'msg': 'подписка отменена'}
    elif not subscription:
        new_subscription = models.Subscription(follower_id=current_user.dict().get('id_user'),
                                               **subscription_data.dict())
        if new_subscription.follower_id == new_subscription.youtuber_id:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail='вы не можете подписаться на себя')
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        return {'msg': 'вы подписались'}


@router.get('/my-subscriptions')
def get_my_subscriptions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    my_subscriptions_id = db.query(models.Subscription.youtuber_id).select_from(models.Subscription).join(
        models.User,
        models.User.id == models.Subscription.follower_id).group_by(
        models.Subscription.youtuber_id).filter(
        models.User.id == current_user.dict().get('id_user')).all()

    lst_of_my_subscriptions_ids = [my_subscriptions_id[i][0] for i in range(len(my_subscriptions_id))]

    my_subscriptions = db.query(models.User).filter(models.User.id.in_(lst_of_my_subscriptions_ids)).all()
    return my_subscriptions


@router.get('/my-subscribers')
def get_my_subscribers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    my_subscribers_id = db.query(models.Subscription.follower_id).select_from(models.Subscription).join(
        models.User,
        models.User.id == models.Subscription.youtuber_id).group_by(
        models.Subscription.follower_id).filter(
        models.User.id == current_user.dict().get('id_user')).all()

    lst_of_my_subscribers_ids = [my_subscribers_id[i][0] for i in range(len(my_subscribers_id))]

    my_subscribers = db.query(models.User).filter(models.User.id.in_(lst_of_my_subscribers_ids)).all()
    return my_subscribers
