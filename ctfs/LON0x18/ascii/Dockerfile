FROM ubuntu:18.04

RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
    python3 \
    socat \
    wamerican \
 && rm -rf /var/lib/apt/lists/*

COPY ascii.py /

CMD ["socat", "-T30", "-d", "-d", "TCP-LISTEN:6000,fork,reuseaddr", "EXEC:'python3 -u ascii.py',pty,echo=0"]

EXPOSE 6000