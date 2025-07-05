FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    iproute2 iptables libnfnetlink-dev libnetfilter-queue-dev \
    gcc build-essential python3-dev tcpdump \
 && pip install --no-cache-dir scapy netfilterqueue

WORKDIR /app
COPY interceptor.py .
CMD ["python", "interceptor.py"]
