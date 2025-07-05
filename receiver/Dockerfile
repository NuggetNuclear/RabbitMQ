# receiver/Dockerfile
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . .

# ① añade nameserver 8.8.8.8 ② instala pika sin usar caché
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf \
 && pip install --no-cache-dir --index-url=https://pypi.org/simple pika

ENTRYPOINT ["python", "-u", "receiver.py"]
