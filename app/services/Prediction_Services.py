from model.prediction import Prediction
from model.schema import PydanticWineDescription
from typing import List
import numpy as np
import joblib
import asyncio


def get_all_predictions(session) -> List[Prediction]:
    return session.query(Prediction).all()


def get_prediction_by_id(prediction_id: int, session) -> Prediction:
    prediction = session.query(Prediction).get(prediction_id)
    return prediction


def get_prediction_by_user(user_id: int, session) -> List[Prediction]:
    predictions = session.query(Prediction).filter(Prediction.user_id == user_id).all()
    return predictions


def create_prediction(new_prediction: Prediction, session) -> None:
    session.add(new_prediction)
    session.commit()
    session.refresh(new_prediction)


async def load_model_async():
    loop = asyncio.get_event_loop()
    model = await loop.run_in_executor(None, joblib.load, 'model/model_RF.pkl')
    return model


async def prediction(wine_data: PydanticWineDescription) -> float:
    model = await load_model_async()
    input_np = np.array([wine_data.fixed_acidity,
                         wine_data.volatile_acidity,
                         wine_data.citric_acid,
                         wine_data.residual_sugar,
                         wine_data.chlorides,
                         wine_data.free_sulfur_dioxide,
                         wine_data.total_sulfur_dioxide,
                         wine_data.density,
                         wine_data.pH,
                         wine_data.sulphates,
                         wine_data.alcohol]).reshape(1, -1)
    result = model.predict(input_np)[0]
    result = float(result)
    return result
