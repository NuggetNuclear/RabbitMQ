FROM python:3.13-slim
RUN apt-get update && apt-get install -y gcc build-essential \
        iptables libnetfilter-queue-dev netcat \
    && pip install --no-cache-dir scapy netfilterqueue
WORKDIR /app
COPY . /app
CMD ["python", "interceptor_nfqueue.py"]
