import pika
import numpy as np
from datetime import datetime
from model.prediction import Prediction
from services import Prediction_Services, Transaction_Services
import json
from database.database import get_session
from rabbit_connection import connection_params
from model.schema import PydanticWineDescription


prediction_price = 100

try:
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    print("Connection established successfully")
except pika.exceptions.AMQPConnectionError as e:
    print(f"Connection failed: {e}")
    exit(1)

prediction_queue_name = "prediction_queue"
result_queue_name = "result_queue"

channel.queue_declare(queue=prediction_queue_name)
channel.queue_declare(queue=result_queue_name)

def callback(ch, method, properties, body):
    '''
    # Печать сырых данных (в байтах)
    print("Received raw body:", body)

    # Декодирование сообщения и печать как строки
    body_str = body.decode('utf-8')
    print("Decoded body as string:", body_str)

    # Попытка преобразовать строку в JSON и печать
    try:
        wine_data = json.loads(body_str)
        print("Parsed JSON data:", wine_data)
    except json.JSONDecodeError:
        print("Failed to decode JSON")
    '''
    wine_data = json.loads(body.decode('utf-8'))
    with next(get_session()) as db:
        user_id = wine_data['user_id']
        wine_description = wine_data['wine_description']

        wine_description_pydantic = PydanticWineDescription(**wine_description)

        result = Prediction_Services.prediction(wine_description_pydantic)

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
        Transaction_Services.decrease(wine_data['user_id'], prediction_price, db)
        prediction_id = new_prediction.prediction_id

    ch.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(
            correlation_id=properties.correlation_id
        ),
        body=str(prediction_id)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_worker():
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=prediction_queue_name, on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == "__main__":
    start_worker()
