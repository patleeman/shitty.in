import requests
import json
import SECRETS
import requests_cache

class Weather(object):
    api_key = SECRETS.FORECASTIO_API_KEY

    def __init__(self):
        self.lat = 40.758932
        self.lng = -73.985131
        self.endpoint = 'https://api.forecast.io/forecast/{api_key}/{lat},{lng}'.format(
            api_key=self.api_key, lat=self.lat, lng=self.lng)

        self.weather_data = {}
        self.forecast = self._get_data()
        self.currently = self.forecast['currently']
        self.scores = self._calculate_current_score()


    def _get_data(self):
        requests_cache.install_cache('weather-cache', backend='sqlite', expire_after=900)
        data = json.loads(requests.get(self.endpoint).text)
        return data

    def _calculate_current_score(self):
        optimal_humidity = [.4, .6]
        optimal_temp = [60, 80]

        current_temp = self.currently['apparentTemperature']
        current_humidity = self.currently['humidity']
        current_precip_prob = self.currently['precipProbability']

        self.weather_data['TEMP'] = int(current_temp)
        self.weather_data['HUMIDITY'] = int(100 * current_humidity)
        self.weather_data['PRECIP_PROBABILITY'] = current_precip_prob

        # Calculate temp score
        if current_temp >= optimal_temp[0] and current_temp <= optimal_temp[1]:
            temp_score = 1
        elif current_temp < optimal_temp[0]:
            temp_score = 1 - ((optimal_temp[0] - current_temp) / optimal_temp[0])
        elif current_temp > optimal_temp[1]:
            temp_score = 1 - ((current_temp - optimal_temp[1]) / optimal_temp[1])
        else:
            raise ValueError("Temp score calculation outside calculable ranges.")

        # Calculate humidity score
        if current_humidity >= optimal_humidity[0] and current_humidity <= optimal_humidity[1]:
            humidity_score = 1
        elif current_humidity > optimal_humidity[1]:
            humidity_score = 1 - (current_humidity - optimal_humidity[1]) / optimal_humidity[1]
        elif current_humidity < optimal_humidity[0]:
            humidity_score = 1 - (optimal_humidity[0] - current_humidity) / optimal_humidity[0]
        else:
            raise ValueError("Temp score calculation outside calculable ranges.")
        # Calculate precip score
        precip_score = 1 - current_precip_prob

        total_score = (100 * ((temp_score * .40) + (humidity_score * .30) + (precip_score * .30)) / 3)

        payload = {
            "TEMP": temp_score,
            "HUMIDITY": humidity_score,
            "PRECIP": precip_score,
            "TOTAL": int(total_score)
        }

        return payload