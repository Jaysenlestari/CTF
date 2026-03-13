FROM python:3.9-slim

RUN apt-get update && \
    apt-get -y install socat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf
WORKDIR /home/ctf

COPY src/main.py /home/ctf/

RUN chown -R root:root /home/ctf && \
    chmod -R 555 /home/ctf

EXPOSE 8889

ENTRYPOINT ["socat", "TCP-LISTEN:8889,reuseaddr,fork,nodelay,su=ctf", "EXEC:'timeout 60 python3 /home/ctf/main.py'"]