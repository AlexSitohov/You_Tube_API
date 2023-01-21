from fastapi import APIRouter, status, Depends, HTTPException

import models
from schemas import User, Wallet, MakeTransaction
from database import get_db
from sqlalchemy.orm import Session
from jwt import get_current_user
from business_logic.make_transaction_logic import transaction

router = APIRouter(tags=['wallets'])


@router.post('/wallets', status_code=status.HTTP_201_CREATED)
def create_wallet(wallet_data: Wallet, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    if db.query(models.Wallet).filter(models.Wallet.user_id == current_user.dict().get('id_user')).first():
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='Кошелек уже существует')
    wallet_new = models.Wallet(**wallet_data.dict(), user_id=current_user.dict().get('id_user'))
    db.add(wallet_new)
    db.commit()
    db.refresh(wallet_new)
    return wallet_new


@router.get('/my-wallet')
def get_my_wallet(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    my_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.dict().get('id_user')).first()
    if not my_wallet:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='У вас нет кошелька')
    return my_wallet


@router.post('/make-transaction', status_code=status.HTTP_201_CREATED)
def make_transaction(transaction_data: MakeTransaction, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    user_id_from = current_user.dict().get('id_user')

    return transaction(user_id_from, transaction_data, db)


@router.get('/checks-to-send')
def checks_to_send(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    my_checks_send = db.query(models.Check).join(models.Wallet, models.Wallet.id == models.Check.wallet_id_from).join(
        models.User, models.User.id == models.Wallet.user_id).group_by(models.Check.id).filter(
        models.User.id == current_user.dict().get(
            'id_user')).all()
    return my_checks_send


@router.get('/checks-to-receive')
def checks_to_receive(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    my_checks_receive = db.query(models.Check).join(models.Wallet,
                                                    models.Wallet.id == models.Check.wallet_id_to).join(
        models.User, models.User.id == models.Wallet.user_id).group_by(models.Check.id).filter(
        models.User.id == current_user.dict().get(
            'id_user')).all()
    return my_checks_receive
