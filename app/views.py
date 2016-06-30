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
    current_temp_f = weather_data.currently['apparentTemperature']
    current_temp_c = (current_temp_f - 32) * (5/9)

    overall_score = int((weather_data.score + transit_data.scores["total"]) / 2)

    payload = {
        "weather": {
            "temp": {
                "f": current_temp_f,
                "c": current_temp_c
            },
            "score": weather_data.score
        },
        "transit": {
            "scores": transit_data.scores,
            "data": transit_data.data
        },
        "overall": overall_score
    }
    return jsonify(payload)

