import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import MakeTransaction, Check


def transaction(user_id_from: int, transaction_data: MakeTransaction, db: Session = Depends(get_db)):
    wallet_from = db.query(models.Wallet).filter(models.Wallet.user_id == user_id_from).first()
    wallet_to = db.query(models.Wallet).filter(models.Wallet.id == transaction_data.wallet_id_to).first()
    wallet_from.balance -= transaction_data.value
    print(wallet_from.balance)
    print(wallet_to.balance)
    if wallet_from.balance < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='не достаточно денег')
    wallet_to.balance += transaction_data.value
    check = models.Check(value=transaction_data.value, date_time_created=datetime.datetime.now(),
                         wallet_id_to=wallet_to.id, wallet_id_from=wallet_from.id)
    db.add(check)
    db.commit()
    db.refresh(wallet_to)
    db.refresh(wallet_from)
    db.refresh(check)
    return check
