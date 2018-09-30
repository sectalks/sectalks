FROM ubuntu:18.04

RUN apt-get update && apt-get upgrade -y && apt-get install --no-install-recommends -y \
    socat \
 && rm -rf /var/lib/apt/lists/*

COPY bewf /
COPY flag.txt /sandbox/

RUN chmod 755 /tmp

USER nobody
WORKDIR sandbox

CMD ["socat", "-T30", "-d", "-d", "TCP-LISTEN:6001,fork,reuseaddr", "EXEC:'/bewf',pty,echo=0,rawer"]

EXPOSE 6001