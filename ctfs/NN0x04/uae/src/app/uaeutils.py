# UAE Utils
import json


def json_encode(value):
    return json.dumps(value)


def json_decode(text):
    return json.loads(text)


def make_response(body, status=200, headers={}, isError=False):
    return {
        "body": body,
        "status": status,
        "headers": headers,
        "errpage": isError
    }


def redirect(url, code=302):
    return make_response(
        "Redirecting to " + url, status=code, headers={"Location": url})


def errorpage(msg, code=500):
    return make_response(msg, status=code, isError=True)
