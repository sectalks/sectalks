FROM ubuntu:18.04

RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
    python3 \
    socat \
 && rm -rf /var/lib/apt/lists/*

COPY electric_maths.py /

CMD ["socat", "-T30", "-d", "-d", "TCP-LISTEN:6003,fork,reuseaddr", "EXEC:'python3 -u electric_maths.py',pty,echo=0"]

EXPOSE 6003