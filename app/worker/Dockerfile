FROM python:3.11-slim

WORKDIR /app/worker

COPY requirements.txt /app/worker/

RUN pip install --upgrade pip && pip install -r /app/worker/requirements.txt

COPY ./ /app/worker/

ENV PYTHONPATH=/app

CMD ["python", "rabbit.py"]