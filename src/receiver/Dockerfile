FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .

RUN pip install pika

CMD ["python", "-u", "receiver.py"]