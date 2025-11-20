FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y socat && \
    pip install py-ecc pycryptodome

COPY src/chall.py .
COPY src/flag.txt .

RUN chmod 600 /app/flag.txt || true
RUN chmod +x /app/chall.py || true

CMD socat TCP-LISTEN:8080,fork,reuseaddr EXEC:"python3 chall.py",stderr