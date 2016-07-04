from flask import render_template, jsonify, redirect, url_for
from app import app
from app.hooks import transit, weather

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
    transit_data = transit.MtaTransit().get_data()
    weather_data = weather.Weather().get_data()
    total_score = int((weather_data['score'] + transit_data['score']) / 2)

    payload = {
        "weather": weather_data,
        "transit": transit_data,
        "overall": total_score,
    }

    return jsonify(payload)

@app.route('/dex/about')
def about():
    return render_template('about.html')