FROM python:3.13-slim
WORKDIR /app
COPY . .
RUN pip install pika
CMD ["python", "sender.py"]
