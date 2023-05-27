import os
from flask import Flask, render_template, render_template_string, request, jsonify
from random import randrange

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.args.get('name'):
        name = request.args.get('name')
        for item in ['.','_','|join','[',']','mro', 'base', '!', '@', '#', '$', '%', '^', '&', '*', '+', '-', '=', ':', ';', '<', '>', '?', '/', ',', '`', '~', ' ']:
            name = name.replace(item, '')
        template = """<!doctype html>
<html>
<head>
	<title>Name to cool factor!</title>
</head>
<body>
	<strong>""" + name + """ is a """ + str(randrange(10)) + """/10 cool name!</strong>
</body>
</html>"""
        return render_template_string(template)
    else:
        return render_template('hello.jinja')

app.debug = False
app.run(host='0.0.0.0', port=8080)
