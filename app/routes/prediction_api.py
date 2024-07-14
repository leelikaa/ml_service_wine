from fastapi import APIRouter, HTTPException, Depends, status
from database.database import get_session
from sqlalchemy.orm import Session
from model.schema import PydanticUsers, PydanticPrediction, PydanticWineDescription
from services import User_Services, Prediction_Services, Transaction_Services
from model.prediction import Prediction
from datetime import datetime

prediction_route = APIRouter(tags=["Prediction"])
prediction_price = 100.0


@prediction_route.post("{id}/predict")
def new_predict(id: int, wine_data: PydanticWineDescription, db: Session = Depends(get_session)):
    user = User_Services.get_user_by_id(id, db)
    user_balance = user.balance
    if user_balance < prediction_price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Don't have enough money, need to add {prediction_price-user_balance}")
    else:
        new_prediction = Prediction(
            user_id=id,
            time=datetime.now(),
            **wine_data.dict()
        )
        result = Prediction_Services.prediction(new_prediction)
        new_prediction.result = result
        Transaction_Services.decrease(id, prediction_price, db)
        Prediction_Services.create_prediction(new_prediction, db)
        return new_prediction.result


@prediction_route.get("{id}/my_predictions")
def user_predictions(id: int, db: Session = Depends(get_session)):
    return Prediction_Services.get_prediction_by_user(id, db)
