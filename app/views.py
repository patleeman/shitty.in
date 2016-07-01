from flask import render_template, jsonify, redirect, url_for
from app import app
from app.service_hooks import transit, weather

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
    weather_data = weather.Weather()
    overall_score = int((weather_data.scores["TOTAL"] + transit_data.total_score) / 2)

    payload = {
        "weather_scores": weather_data.scores,
        "weather_data": weather_data.weather_data,
        "transit": transit_data.scores,
        "transit_score": transit_data.total_score,
        "overall": overall_score,
    }

    return jsonify(payload)

@app.route('/dex/about')
def about():
    return render_template('about.html')