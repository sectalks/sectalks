from flask import Flask
import os

HOST = 'unhackable.app'
SERVER_NAME = 'Unhackable App Engine'


class uaeFlask(Flask):
    def process_response(self, response):
        super(uaeFlask, self).process_response(response)
        response.headers['Server'] = SERVER_NAME
        return (response)


app = uaeFlask(__name__)
app.config['SERVER_NAME'] = HOST
app.secret_key = os.environ["FLASK_SECRET_KEY"]

from app import routes
print("uae init")
