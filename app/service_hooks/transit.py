import xmltodict
import requests
import datetime

class MtaTransit(object):

    def __init__(self):
        self.endpoint = "http://web.mta.info/status/serviceStatus.txt"
        self.data = self._get_data()

    def _get_data(self):
        raw_xml_data = requests.get(self.endpoint).text
        data = xmltodict.parse(raw_xml_data, dict_constructor=dict)
        response_code = data['service']['responsecode']

        if int(response_code) == 0:
            payload = {
                'subway': self._parse_transit(data['service']['subway']),
                'bus': self._parse_transit(data['service']['bus']),
                'bt': self._parse_transit(data['service']['BT']),
                'lirr': self._parse_transit(data['service']['LIRR']),
                'metronorth': self._parse_transit(data['service']['MetroNorth']),
                'timestamp': datetime.datetime.strptime(data['service']['timestamp'], "%m/%d/%Y %I:%M:%S %p")
            }

        else:
            payload = None
            #TODO: Raise a warning that response code was non-zero

        return payload


    @staticmethod
    def _parse_transit(data):
        transit_payload = {}
        for transit_line in data['line']:
            line = transit_line.get('name')
            status = transit_line.get('status')
            time = transit_line.get('Time')
            text = transit_line.get('text')

            transit_payload[line] = {
                'status': status,
                'time': time,
                'text': text
            }
        return transit_payload

