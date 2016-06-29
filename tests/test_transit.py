import unittest
from app.service_hooks import transit

class TestTransit(unittest.TestCase):

    def test_transit_api_call(self):
        transit_instance = transit.MtaTransit()
        self.assertIsInstance(transit_instance.data, dict)


if __name__ == '__main__':
    unittest.main()

