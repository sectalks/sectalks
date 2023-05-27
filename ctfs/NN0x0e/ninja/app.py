#!/usr/bin/env python3

import requests
from flask import Flask, request, abort, render_template_string
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3

app = Flask(__name__)
limiter = Limiter(get_remote_address, app = app)

newpost = '''
<head>
    <title>Ninja</title>
</head>
<style>
    body {
        width: 50em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
<body>
<h2>Create A New Post</h2>
<p>This page is under development. Currently only you will be able to preview the post.</p>
<form action="/submit" name="postForm" method="post">
    <textarea id="confirmationText" class="text" cols="86" rows ="20" name="postForm"></textarea>
    <br>
    <input type="submit" value="Preview Post" >
</form>
</body>
'''

mainpage = '''
<head>
    <title>Ninja</title>
</head>
<style>
    body {
        width: 50em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
<body>
<h2>Main Page</h2>
<p>Welcome to our site! Currently we're using this framework called Flask that uses a <b>template engine</b> called Jinja2!</p>
<a href="/newpost">Make a new post</a> 
</body>
'''

@app.route('/')
def indexpage():
  return mainpage
  
@app.route('/newpost')
def newpostpage():
  return newpost

@app.route('/submit', methods=['POST'])
@limiter.limit("10/minute") 
def submitpage():
    try:
        message = request.form['postForm']
        template = '''message preview: {}'''.format(message)
        return render_template_string(message)
    except:
        return 'Error!'

app.run(host='0.0.0.0', port=5004, threaded=True)
