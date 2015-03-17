# docker build -t sectalks/syd0x05 .
# docker run -d sectalks/syd0x05
# docker exec -it <id> sudo -i -u ctf

FROM ubuntu:14.04
MAINTAINER "Aleksa Sarai <cyphar@cyphar.com>"

# Install packages.
RUN dpkg --add-architecture i386
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y build-essential python python-pip mercurial supervisor perl libc6:i386 lib32ncurses5 libstdc++6:i386 dash golang vim nano zsh
RUN pip install hg+https://bitbucket.org/dbenamy/devcron#egg=devcron

# Set up supervisor.
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Set up users.
RUN useradd -s/bin/bash -m -d/home/gl4dl0gs -- gl4dl0gs
RUN passwd -l -- gl4dl0gs
RUN useradd -s/bin/bash -m -d/home/ctf -- ctf
RUN passwd -d -- ctf

# Set up flag.
COPY flag /flag
RUN chown root:root /flag && chmod 400 /flag

# Make build dirs.
RUN mkdir -p /src

# 01: Set up s3cur3s4f3.
COPY 01-s3cur3s4f3/ /src/s3cur3s4f3
RUN cp -v /src/s3cur3s4f3/s3cur3s4f3 /home/ctf/s3cur3s4f3 && \
	chmod 111 /home/ctf/s3cur3s4f3
RUN cd /src/s3cur3s4f3/ && go build w00t.go && \
	cp -v /src/s3cur3s4f3/w00t /home/ctf/w00t && \
	chmod 111 /home/ctf/w00t && \
	chown gl4dl0gs:gl4dl0gs /home/ctf/w00t && \
	chmod u+s /home/ctf/w00t

# 02: Set up gl4d0s.
COPY 02-gl4d0s/ /src/gl4d0s
RUN cd /src/gl4d0s/ && make clean all && make install {SUSER,SGROUP}=root {LUSER,LGROUP}=gl4dl0gs
RUN mkdir /cron && \
	echo "* * * * * /cron/gl4d0s.sh" > /cron/crontab && \
	cp -v /src/gl4d0s/cron/gl4d0s.sh /cron/gl4d0s.sh

# Clean up build dirs -- we don't want the source code to be lying around.
RUN rm -rf /src

# Set up environment for server.
# The actual user will shell into the environment with "docker exec", using docksh.
ENTRYPOINT ["/usr/bin/supervisord"]
