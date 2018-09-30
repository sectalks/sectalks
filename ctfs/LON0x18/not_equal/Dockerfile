FROM ubuntu:18.04

RUN dpkg --add-architecture i386 && \
    apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
    libc6:i386 \
    socat \
 && rm -rf /var/lib/apt/lists/*

COPY not_equal /
COPY flag.txt /sandbox/

RUN chmod 755 /tmp

USER nobody
WORKDIR sandbox

CMD ["socat", "-T30", "-d", "-d", "TCP-LISTEN:6004,fork,reuseaddr", "EXEC:'/not_equal',pty,echo=0,rawer"]

EXPOSE 6004