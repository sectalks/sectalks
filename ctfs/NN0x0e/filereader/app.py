from flask import Flask, request, render_template
import os

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        path = request.form.get('path')
        path = os.path.abspath(path)
        if os.path.isfile(path):
            with open(path, 'r') as f:
                content = f.read()
                return render_template('file_content.html', content = content)
        else:
            return render_template('invalid_path.html')
    else:
        return render_template('index.html')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
