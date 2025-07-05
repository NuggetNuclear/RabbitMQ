FROM python:3.12-slim

RUN apt-get update && apt-get install -y iproute2 iptables libnfnetlink-dev libnetfilter-queue-dev tcpdump \
    && pip install --no-cache-dir scapy netfilterqueue

WORKDIR /app
COPY interceptor.py .
CMD ["python", "-u","interceptor.py"]
