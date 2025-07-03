# ./sender/Dockerfile
FROM python:3.12-slim

# des-bufferiza TODO
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY sender_cli.py .

RUN pip install pika

ENTRYPOINT ["python", "-u", "sender_cli.py"]
