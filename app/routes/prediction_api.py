from fastapi import APIRouter, HTTPException, Depends, status
from database.database import get_session
from sqlalchemy.orm import Session
from model.schema import PydanticUsers, PydanticPrediction, PydanticWineDescription
from services import User_Services, Prediction_Services, Transaction_Services
import asyncio
from rabbit import channel, queue_name
from sqlalchemy.orm.exc import NoResultFound
import json

prediction_route = APIRouter(tags=["Prediction"])
prediction_price = 100.0
exchange_name = queue_name

channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
result_queue = channel.queue_declare('', exclusive=True)
result_queue_name = result_queue.method.queue
channel.queue_bind(exchange=exchange_name, queue=result_queue_name, routing_key=result_queue_name)


@prediction_route.post("{id}/predict")
async def new_predict(id: int, wine_data: PydanticWineDescription, db: Session = Depends(get_session)):
    try:
        user = User_Services.get_user_by_id(id, db)
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")

    user_balance = user.balance
    if user_balance < prediction_price:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Don't have enough money, need to add {prediction_price-user_balance}")
    else:
        channel.basic_publish(
            exchange=exchange_name,
            routing_key='ml_tasks',
            body=json.dumps({
                "user_id": id,
                "wine_description": wine_data.dict
            }),
            properties=pika.BasicProperties(
                reply_to=result_queue_name,
                correlation_id=str(id)
            )
        )

        return {"message": "Prediction task sent."}


@prediction_route.get("{id}/my_predictions")
def user_predictions(id: int, db: Session = Depends(get_session)):
    method, properties, body = channel.basic_get(queue=result_queue_name, auto_ack=True)

    if body is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Result not found.")

    if properties.correlation_id != str(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Correlation ID does not match.")

    prediction_id = int(body.decode())
    prediction = Prediction_Services.get_prediction_by_id(prediction_id, db)
    return prediction
