import unittest
from app.hooks import transit
from pprint import pprint

class TestTransit(unittest.TestCase):
    def setUp(self):
        self.transit_instance = transit.MtaTransit()
        pprint(self.transit_instance.payload)

    def test_transit_api_call(self):
        self.assertIsInstance(self.transit_instance.get_data(), dict)


if __name__ == '__main__':
    unittest.main()

