import unittest
from app.hooks import weather
from pprint import pprint


class TestWeather(unittest.TestCase):
    def setUp(self):
        self.obj_inst = weather.Weather()
        pprint(self.obj_inst.scores)

    def test_weather_api_call(self):
        self.assertIsInstance(self.obj_inst.forecast, dict)

    def test_weather_score(self):
        self.assertIsInstance(self.obj_inst.scores, dict)


if __name__ == '__main__':
    unittest.main()

