import unittest
from app.service_hooks import weather
from pprint import pprint


class TestWeather(unittest.TestCase):
    def setUp(self):
        self.obj_inst = weather.Weather()
        pprint(self.obj_inst.forecast)

    def test_weather_api_call(self):
        self.assertIsInstance(self.obj_inst.forecast, dict)



if __name__ == '__main__':
    unittest.main()

