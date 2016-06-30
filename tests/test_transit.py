import unittest
from app.service_hooks import transit
from pprint import pprint

class TestTransit(unittest.TestCase):
    def setUp(self):
        self.transit_instance = transit.MtaTransit()
        pprint(self.transit_instance.total_score)

    def test_transit_api_call(self):
        self.assertIsInstance(self.transit_instance.data, dict)

    def test_transit_calculate_score(self):
        self.assertIsInstance(self.transit_instance.scores, dict)


if __name__ == '__main__':
    unittest.main()

