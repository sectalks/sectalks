FROM ubuntu:18.04

RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
    python3 \
    socat \
 && rm -rf /var/lib/apt/lists/*

COPY cerberus.py /

CMD ["socat", "-d", "-d", "TCP-LISTEN:6002,fork,reuseaddr", "EXEC:'python3 -u cerberus.py',pty,echo=0"]

EXPOSE 6002