FROM python:3.12-slim

RUN apt-get update && apt-get install -y tcpdump iproute2 iputils-ping \
    && pip install --no-cache-dir scapy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY sniffer.py ./
CMD ["python", "sniffer.py"]
