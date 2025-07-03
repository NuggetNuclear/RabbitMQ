FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1          # no buffering ever
WORKDIR /app
COPY sender_cli.py .
RUN pip install pika
ENTRYPOINT ["python", "-u", "sender_cli.py"]   # -u extra unbuffered
