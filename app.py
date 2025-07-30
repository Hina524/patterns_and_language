from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js', mimetype='application/javascript')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css', mimetype='text/css')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000) 