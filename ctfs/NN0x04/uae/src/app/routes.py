from flask import Response, request, make_response, render_template, session, redirect, flash, send_file
import requests
import yaml
from urlparse import urlparse
from mss import MSSClient
from app import app
from uaerunner import runCode, flattenRequest
import uaeutils
import random
import string
import os

CACHE_EXPIRES = 300  # 5 min
REQUEST_TIMEOUT = 3  # seconds

mssc = MSSClient()


def strip_scheme(url):
    parsed = urlparse(url)
    scheme = "%s://" % parsed.scheme
    return parsed.geturl().replace(scheme, '', 1)


def error(code, message="That was an error. Please try again later.",
          debug=""):
    return render_template(
        "error.html", code=code, message=message, debug=debug), code


@app.route('/')
@app.route('/', subdomain='www')
def landing():
    return render_template("landing.html")


@app.route(
    '/f7850386-f8a4-42a1-91a8-b19edb68fd5a/code.tgz', subdomain="manage")
def downcode():
    return send_file("/code.tgz")


@app.route('/', subdomain="manage")
def manage():
    if "username" not in session:
        return redirect("/login")
    return render_template("manage.html", username=session["username"])


@app.route('/login', subdomain="manage", methods=['GET', 'POST'])
def login():
    if "username" in session:
        return redirect("/")
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]
    if len(password) < 3 or len(username) < 3:
        flash("username and password should be longer than 3 characters",
              "danger")
        return render_template("login.html")
    rp = mssc.get("user/" + username)
    if rp == "":  # register new user
        mssc.set("user/" + username, password)
    else:
        if rp != password:
            flash("wrong password", "danger")
            return render_template("login.html")
    session["username"] = username
    return redirect("/")


@app.route('/edit', subdomain="manage", methods=['GET', 'POST'])
def edit():
    if "username" not in session:
        return redirect("/login")
    username = session["username"]
    userapp = request.args.get('app')
    owner = mssc.get("owner/" + userapp)
    if owner == "":
        mssc.set("owner/" + userapp, username)
    elif owner != username:
        flash(
            "You don't have permission to edit " + userapp +
            ".unhackable.app because you didn't create it.", "danger")
        return render_template("manage.html", username=username)
    if not userapp:
        return error(400, message="wrong parameter")
    if request.method == "GET":
        return render_template(
            "edit.html", userapp=userapp, code=mssc.get("code/" + userapp))
    if request.method == "POST":
        code = request.form["code"]
        decoded = yaml.safe_load(code)
        if "urls" not in decoded:
            return error(400, message="missing urls")
        if "default_handler" not in decoded:
            return error(400, message="missing default_handler")
        for url in decoded['urls']:
            if not url.startswith("/"):
                return error(400, message="%s must start with /" % url)
        for url, code in decoded['urls'].items():
            mssc.set(
                "cache/" + userapp + '.' + app.config['SERVER_NAME'] + url,
                code, CACHE_EXPIRES)
        mssc.set("code/" + userapp, request.form["code"])
        return render_template(
            "edit.html",
            userapp=userapp,
            code=mssc.get("code/" + userapp),
            msg="Updated!")


@app.route('/flag', subdomain="manage", methods=['GET', 'POST'])
def viewflag():
    if "otp" not in session:
        session["otp"] = ''.join([
            random.choice(string.ascii_letters + string.digits)
            for n in xrange(32)
        ])
    if request.method == "GET":
        return render_template("flag.html", otp=session["otp"])
    url = request.form["url"]
    if not url.startswith("https://otp.unhackable.app/"):
        return error(400,
                     "OTP URL must start with https://otp.unhackable.app/")
    rsp = requests.get(url).text.encode("utf-8")
    if session["otp"] in rsp:
        return os.environ["CTF_FLAG"]
    else:
        return error(403, url + " does not contain " + session["otp"])

@app.route('/<path:path>', subdomain="manage", methods=['GET', 'POST'])
@app.route('/<path:path>', subdomain="www", methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def reserved404(path):
    return error(404, "page not found")


@app.route(
    '/', subdomain="<userapp>", defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', subdomain="<userapp>", methods=['GET', 'POST'])
def runapp(path, userapp):
    try:
        code = mssc.get("cache/" + strip_scheme(request.base_url))
        if code is None or code == "":
            sitecode = mssc.get("code/" + userapp)
            if sitecode is None or sitecode == "":
                return error(
                    404,
                    message="The requested URL %s was not found on this server."
                    % request.path)
            decoded = yaml.safe_load(mssc.get("code/" + userapp))
            if request.path in decoded['urls']:
                code = decoded['urls'][request.path]
            else:
                code = decoded['default_handler']
            mssc.set("cache/" + request.base_url, code, CACHE_EXPIRES)

        result = runCode({
            'request': flattenRequest(request),
            'uaeutils': uaeutils
        }, code, REQUEST_TIMEOUT)
        if not result:
            return error(502, message="The server didn't return anything.")
        if type(result) == unicode:
            return error(500, debug=result.encode('utf-8'))
        if type(result) != dict:
            return error(500, message="Please use uaeutils to generate uae_rsp")
        if type(result['body']) != str:
            return error(500, message="Body must be str")
        if type(result['status']) != int:
            return error(500, message="Status must be int")
        if result['errpage']:
            rsp = make_response(
                error(result['status'], message=result['body']))
        else:
            rsp = make_response(result['body'], result['status'])
        for k, v in result['headers'].items():
            if type(k) != str or type(v) != str:
                return error(500, message="Header K/Vs must be str")
            rsp.headers[k] = v
        return rsp
    except Exception as e:
        return error(500, debug=str(e))
