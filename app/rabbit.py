import pika
import numpy as np
from datetime import datetime
from model.prediction import Prediction
from services import Prediction_Services, Transaction_Services
import json
from database.database import get_session
from sqlalchemy.orm import Session
from fastapi import Depends
from dotenv import load_dotenv
import os

load_dotenv('.env')

username = os.getenv("RABBIT_USER", "rmuser")
password = os.getenv("RABBIT_PASSWORD", "rmpassword")

prediction_price = 100

connection_params = pika.ConnectionParameters(
    host='rabbitmq',
    virtual_host='/',
    credentials=pika.PlainCredentials(
        username=username,
        password=password
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

queue_name = "prediction_queue"
channel.queue_declare(queue=queue_name)


def callback(ch, method, properties, body):
    db = next(get_session())

    wine_data = json.loads(body.decode('utf-8'))

    user_id = wine_data['user_id']
    wine_description = wine_data['wine_description']

    input_np = np.array([
        wine_description['fixed_acidity'],
        wine_description['volatile_acidity'],
        wine_description['citric_acid'],
        wine_description['residual_sugar'],
        wine_description['chlorides'],
        wine_description['free_sulfur_dioxide'],
        wine_description['total_sulfur_dioxide'],
        wine_description['density'],
        wine_description['pH'],
        wine_description['sulphates'],
        wine_description['alcohol']
    ]).reshape(1, -1)

    result = Prediction_Services.prediction(input_np)

    new_prediction = Prediction(
        user_id=user_id,
        time=datetime.now(),
        fixed_acidity=wine_description['fixed_acidity'],
        volatile_acidity=wine_description['volatile_acidity'],
        citric_acid=wine_description['citric_acid'],
        residual_sugar=wine_description['residual_sugar'],
        chlorides=wine_description['chlorides'],
        free_sulfur_dioxide=wine_description['free_sulfur_dioxide'],
        total_sulfur_dioxide=wine_description['total_sulfur_dioxide'],
        density=wine_description['density'],
        pH=wine_description['pH'],
        sulphates=wine_description['sulphates'],
        alcohol=wine_description['alcohol'],
        result=float(result))

    Prediction_Services.create_prediction(new_prediction, db)

    channel.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=str(new_prediction.prediction_id)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    Transaction_Services.decrease(wine_data['user_id'], prediction_price, db)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='prediction_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
