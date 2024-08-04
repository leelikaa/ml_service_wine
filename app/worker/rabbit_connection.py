import pika
from dotenv import load_dotenv
import os


load_dotenv('.envdb')

username = os.getenv("RABBITMQ_DEFAULT_USER", "rmuser")
password = os.getenv("RABBITMQ_DEFAULT_PASS", "rmpassword")

print(f"RabbitMQ Username: {username}, password {password}")

connection_params = pika.ConnectionParameters(
    host='rabbitmq',
    virtual_host='/',
    port=5672,
    credentials=pika.PlainCredentials(
        username=username,
        password=password
    ),
    heartbeat=30,
    blocked_connection_timeout=2
)
