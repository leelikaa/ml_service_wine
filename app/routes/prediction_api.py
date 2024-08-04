from fastapi import APIRouter, HTTPException, Depends, status
from database.database import get_session
from sqlalchemy.orm import Session
from model.schema import PydanticUsers, PydanticPrediction, PydanticWineDescription
from services import User_Services, Prediction_Services, Transaction_Services
from model.prediction import Prediction
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
import json
import pika
import os
from auth.dependencies import get_current_user
from services.logging_config import get_logger
from worker.rabbit_connection import connection_params

logger = get_logger(logger_name=__name__)

prediction_route = APIRouter(tags=["Prediction"])
prediction_price = 100.0


def get_rabbitmq_connection():
    return pika.BlockingConnection(connection_params)


def publish_message(exchange_name: str, routing_key: str, body: dict, reply_to: str, correlation_id: str):
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue=routing_key)
    body_str = json.dumps(body)
    print(f"Publishing message to routing_key '{routing_key}': {body_str}")
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        body=body_str,
        properties=pika.BasicProperties(
            reply_to=reply_to,
            correlation_id=correlation_id
        )
    )
    connection.close()


@prediction_route.post("{id}/predict")
def new_predict(id: int, wine_data: PydanticWineDescription, db: Session = Depends(get_session), user: int = Depends(get_current_user)):
    logger.info(f"Received prediction request for user_id={id}")
    logger.info(f"Token: {user}")

    if id != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized. Pls use /user/signin")
    try:
        user = User_Services.get_user_by_id(id, db)
    except NoResultFound:
        logger.error(f"User with id {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    user_balance = user.balance
    if user_balance < prediction_price:
        logger.error(f"Insufficient funds for user_id {id}. Need {prediction_price - user_balance}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Don't have enough money, need to add {prediction_price-user_balance}")
    else:
        routing_key = 'prediction_queue'
        reply_to = "result_queue"
        correlation_id = str(id)

        publish_message(
            exchange_name='',
            routing_key=routing_key,
            body={
                "user_id": id,
                "wine_description": wine_data.dict()
            },
            reply_to=reply_to,
            correlation_id=correlation_id
        )
        logger.info(f"Prediction task sent for user_id {id}")
        return {"message": "Prediction task sent."}


@prediction_route.get("{id}/my_predictions")
def user_predictions(id: int, db: Session = Depends(get_session), user: int = Depends(get_current_user)):
    logger.info(f"Fetching predictions for user_id={id}")
    logger.info(f"Token: {user}")

    if id != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized. Pls use /user/signin")

    try:
        prediction = Prediction_Services.get_prediction_by_user(id, db)
    except NoResultFound:
        logger.error(f"No predictions found for user_id {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No predictions found for user_id {id}")
    return prediction
