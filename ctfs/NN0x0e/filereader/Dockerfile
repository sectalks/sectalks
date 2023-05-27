FROM python:3.9-slim-buster

WORKDIR app

COPY . .

RUN pip3 install -r requirements.txt
 
RUN useradd -m flag && echo "flag:qwerty123" | chpasswd

CMD ["python3", "app.py"]

