FROM python:3.13-slim

RUN apt-get update && apt-get install -y tcpdump \
    && pip install --no-cache-dir scapy

WORKDIR /app
COPY sniffer.py .
CMD ["python", "sniffer.py"]
