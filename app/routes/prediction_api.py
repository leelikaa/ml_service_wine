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
from auth.jwt_handler import create_access_token, verify_access_token, oauth2_scheme

prediction_route = APIRouter(tags=["Prediction"])
prediction_price = 100.0

rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
rabbitmq_port = int(os.getenv("RABBITMQ_PORT", 5672))
rabbitmq_user = os.getenv("RABBITMQ_USER", "rmuser")
rabbitmq_password = os.getenv("RABBITMQ_PASSWORD", "rmpassword")


def get_rabbitmq_connection():
    connection_params = pika.ConnectionParameters(
        host=rabbitmq_host,
        port=rabbitmq_port,
        credentials=pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
    )
    return pika.BlockingConnection(connection_params)


def publish_message(exchange_name: str, routing_key: str, body: dict, reply_to: str, correlation_id: str):
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue=routing_key)
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        body=json.dumps(body),
        properties=pika.BasicProperties(
            reply_to=reply_to,
            correlation_id=correlation_id
        )
    )
    connection.close()


@prediction_route.post("{id}/predict")
def new_predict(id: int, wine_data: PydanticWineDescription, db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    verify_access_token(token)

    try:
        user = User_Services.get_user_by_id(id, db)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    user_balance = user.balance
    if user_balance < prediction_price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Don't have enough money, need to add {prediction_price-user_balance}")
    else:
        exchange_name = 'prediction_exchange'
        routing_key = 'ml_tasks'
        reply_to = "prediction_queue"
        correlation_id = str(id)

        publish_message(
            exchange_name=exchange_name,
            routing_key=routing_key,
            body={
                "user_id": id,
                "wine_description": wine_data.dict()
            },
            reply_to=reply_to,
            correlation_id=correlation_id
        )
        return {"message": "Prediction task sent."}


@prediction_route.get("{id}/my_predictions")
def user_predictions(id: int, db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    verify_access_token(token)

    try:
        prediction = Prediction_Services.get_prediction_by_user(id, db)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found.")
    return prediction

