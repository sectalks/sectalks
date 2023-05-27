FROM ubuntu:latest

RUN apt update -y && apt install -y ssh
RUN addgroup ftp
RUN useradd -m anonymous -g ftp && echo "anonymous:anonymous" | chpasswd

ADD sshd_config /etc/ssh/sshd_config
ADD note /home/anonymous/note

RUN mkdir -p /run/sshd
RUN chown root:root /home/anonymous/
RUN chmod 755 /home/anonymous

CMD ["/usr/sbin/sshd", "-D", "-e"]
