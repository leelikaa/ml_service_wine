from model.schema import Prediction
from typing import List
import numpy as np
import joblib


def get_all_predictions(session) -> List[Prediction]:
    return session.query(Prediction).all()


def get_prediction_by_id(prediction_id: int, session) -> Prediction:
    predictions = session.get(Prediction, prediction_id)
    if predictions:
        return predictions
    return None


def get_prediction_by_user(user_id: int, session) -> Prediction:
    predictions = session.query(Prediction).filter(Prediction.user_id == user_id)
    if predictions:
        return predictions
    return None


def create_prediction(new_prediction: Prediction, session) -> None:
    session.add(new_prediction)
    session.commit()
    session.refresh(new_prediction)


def prediction(wine_data) -> float:
    wine_input = wine_data.dict()
    model = joblib.load('model/model_RF.pkl')
    input_np = np.array(list(wine_input.values())).reshape(1, -1)
    result = model.predict(input_np)[0]
    return result
