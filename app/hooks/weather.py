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
        data = self._get_data()
        currently = data['currently']
        today = data['daily']['data'][0]
        self.payload = self._process_weather(currently, today)
        return self.payload

    def _get_data(self):
        requests_cache.install_cache('weather-cache', backend='sqlite', expire_after=900)
        data = json.loads(requests.get(self.endpoint).text)
        return data


    def _process_weather(self, currently, today):
        optimal_humidity = [.4, .6]
        optimal_temp = [60, 80]

        current_temp = currently['apparentTemperature']
        high_temp = today['temperatureMax']
        low_temp = today['temperatureMin']
        current_humidity = currently['humidity']
        precip = today['precipProbability']

        payload = {}
        payload['temp'] = {'value': int(current_temp)}
        payload['high_temp'] = {'value': int(high_temp)}
        payload['low_temp'] = {'value': int(low_temp)}
        payload['humidity'] = {'value': int(100 * current_humidity)}
        payload['precip'] = {'value': int(100* precip)}

        # Calculate current temp score
        temp_score = self._calculate_weather_score(current_temp, optimal_temp[0], optimal_temp[1])
        payload["temp"]['score'] = int(temp_score * 100)

        # Calculate high temp score
        high_temp_score = self._calculate_weather_score(high_temp, optimal_temp[0], optimal_temp[1])
        payload["high_temp"]['score'] = int(high_temp_score * 100)

        # Calculate low temp score
        low_temp_score = self._calculate_weather_score(low_temp, optimal_temp[0], optimal_temp[1])
        payload["low_temp"]['score'] = int(low_temp_score * 100)

        # Calculate humidity score
        humidity_score = self._calculate_weather_score(current_humidity, optimal_humidity[0], optimal_humidity[1])
        payload['humidity']['score'] = int(humidity_score * 100)

        # Calculate precip score
        payload["precip"]['score'] = int(precip * 100)
        payload['precip']['type'] = today.get('precipType', '')

        total_score = (temp_score * .15) \
                      + (high_temp_score * .20) \
                      + (low_temp_score * .05) \
                      + (humidity_score * .20) \
                      + (precip * .40)

        payload['score'] = int(total_score * 100)

        # Additional items
        payload['current_summary'] = currently['summary']
        payload['today_summary'] = today['summary']

        return payload
    
    @staticmethod
    def _calculate_weather_score(metric, min, max):
        if metric >= min and metric <= max:
            score = 0
        elif metric < min:
            score = (min - metric) / min
        elif metric > max:
            score = (metric - max) / max
        else:
            raise ValueError("Temp score calculation outside calculable ranges.")

        return score