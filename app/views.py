from flask import render_template, jsonify
from app import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/data', methods=['GET'])
def data_endpoint():
    data = {
        "data": [{"data": "One"}, {"data": "Two"}, {"data": "Three"}]
    }
    return jsonify(data)

