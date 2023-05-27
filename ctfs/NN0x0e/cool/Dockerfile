FROM python:3

RUN mkdir /ctf
WORKDIR /ctf
RUN useradd -M -d /ctf ctf

COPY app /ctf/app
WORKDIR /ctf/app
RUN pip install -r requirements.txt
RUN chmod ugo+x /ctf/app/run.sh
CMD ["su", "-", "ctf", "-c", "/ctf/app/run.sh"]
EXPOSE 8080
