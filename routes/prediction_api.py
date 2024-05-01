from fastapi import APIRouter, HTTPException, Depends, status
from database.database import SessionLocal
from sqlalchemy.orm import Session

from model.schema import Users, Prediction, WineDescription
from services import User_Services, Prediction_Services


def get_db():
    with SessionLocal() as db:
        return db


prediction_router = APIRouter(tags=["Prediction"])
prediction_price = 100.0


@prediction_router.post("{id}/predict")
def new_predict(id: int, wine_data: WineDescription, db: Session = Depends(get_db)):
    user_balance = User_Services.get_user_by_id(id, db).balance
    if user_balance < prediction_price:
        raise HTTPException(status_code=400, detail=f"Don't have enough money, need to add {prediction_price-user_balance}")
    else:
        result = Prediction_Services.prediction(wine_data)
        #закончить функцию с добавлением транзакции по списанию, изменению баланса юзера и результата модели в соответсвующие таблицы


@prediction_router.get("{id}/my_predictions")
def user_predictions(id: int, db: Session = Depends(get_db)):
    return Prediction_Services.get_prediction_by_user(id, db)