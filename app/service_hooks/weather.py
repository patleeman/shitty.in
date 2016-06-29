import forecastio
import SECRETS


class Weather(object):
    api_key = SECRETS.FORECASTIO_API_KEY
    lat = 40.758932
    lng = -73.985131

    def __init__(self):
        self.forecast = forecastio.load_forecast(self.api_key, self.lat, self.lng)


