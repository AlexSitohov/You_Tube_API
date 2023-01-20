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
    wallet_new = models.Wallet(**wallet_data.dict(), user_id=current_user.dict().get('id_user'))
    db.add(wallet_new)
    db.commit()
    db.refresh(wallet_new)
    return wallet_new


@router.post('/make-transaction', status_code=status.HTTP_201_CREATED)
def make_transaction(transaction_data: MakeTransaction, db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    user_id_from = current_user.dict().get('id_user')

    return transaction(user_id_from, transaction_data, db)
