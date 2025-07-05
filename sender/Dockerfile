FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .

RUN pip install pika

ENTRYPOINT ["python", "-u", "sender.py"]