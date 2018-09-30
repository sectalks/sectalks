from flask import Flask
from flask import request
from flask import Response
app = Flask(__name__)

flag = 'STL{abounding_defective_teeth}'

@app.route("/somesite/", methods=['GET', 'POST'])
def hello():
    if request.values['name'] == 'admin' and request.values['password'] == 'rosebud':
        return 'It\'s your lucky day! Here it is: {}'.format(flag)
    else:
        return 'Sorry, wrong! Please try again.'