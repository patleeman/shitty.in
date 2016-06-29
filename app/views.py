from flask import render_template, jsonify, redirect, url_for
from app import app
from app.service_hooks import transit

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('dex'))

@app.route('/dex')
def dex():
    return render_template('index.html')

@app.route('/dex/nyc')
def nyc():
    return render_template('nyc.html')

@app.route('/api', methods=['GET'])
def data_endpoint():
    transit_data = transit.MtaTransit()

    payload = {
        "weather": {
            "temp": {
                "f": 75,
                "c": 24
            }},
        "transit": transit_data.data,
    }
    return jsonify(payload)

