FROM python:3.13-slim
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && \
    apt-get update && apt-get install -y gcc build-essential \
        iptables libnetfilter-queue-dev && \
    pip install --no-cache-dir scapy netfilterqueue pika
WORKDIR /app
COPY . /app
CMD ["python", "interceptor_nfqueue.py"]
