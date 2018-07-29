from flask import Flask
from flask import request
from flask import Response
app = Flask(__name__)

@app.route("/")
def hello():
    print(request.headers)

    if 'Android' not in request.headers.get('User-Agent'):
        return Response("Only connections from Android permitted", 401)

    resp = Response("Hello World!")
    if request.headers.get('X-Admin') == 'True':
        resp.headers['X-flag3'] = 'flag{integrated_native_safari}'
    return resp
