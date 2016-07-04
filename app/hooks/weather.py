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
        self.payload = None


    def get_data(self):
        currently = self._get_data()['currently']
        self.payload = self._process_currently(currently)
        return self.payload

    def _get_data(self):
        requests_cache.install_cache('weather-cache', backend='sqlite', expire_after=900)
        data = json.loads(requests.get(self.endpoint).text)
        return data


    def _process_currently(self, currently):
        optimal_humidity = [.4, .6]
        optimal_temp = [60, 80]

        current_temp = currently['apparentTemperature']
        current_humidity = currently['humidity']
        current_precip = currently['precipProbability']

        payload = {}
        payload['temp'] = {'value': int(current_temp)}
        payload['humidity'] = {'value': int(100 * current_humidity)}
        payload['precip'] = {'value': current_precip}

        # Calculate temp score
        if current_temp >= optimal_temp[0] and current_temp <= optimal_temp[1]:
            temp_score = 0
        elif current_temp < optimal_temp[0]:
            temp_score = (optimal_temp[0] - current_temp) / optimal_temp[0]
        elif current_temp > optimal_temp[1]:
            temp_score = (current_temp - optimal_temp[1]) / optimal_temp[1]
        else:
            raise ValueError("Temp score calculation outside calculable ranges.")
        payload["temp"]['score'] = int(temp_score * 100)

        # Calculate humidity score
        if current_humidity >= optimal_humidity[0] and current_humidity <= optimal_humidity[1]:
            humidity_score = 0
        elif current_humidity > optimal_humidity[1]:
            humidity_score = (current_humidity - optimal_humidity[1]) / optimal_humidity[1]
        elif current_humidity < optimal_humidity[0]:
            humidity_score = (optimal_humidity[0] - current_humidity) / optimal_humidity[0]
        else:
            raise ValueError("Temp score calculation outside calculable ranges.")
        payload['humidity']['score'] = int(humidity_score * 100)

        # Calculate precip score
        precip_score = payload['precip']['value']
        payload["precip"]['score'] = int(precip_score * 100)

        total_score = (temp_score * .40) + (humidity_score * .30) + (precip_score * .30)

        payload['score'] = int(total_score * 100)

        return payload