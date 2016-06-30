"""
transit.py
MTA Service Status

Requests and parses the NYC MTA's service status.  Then calculates the shitty score.

"""

import xmltodict
import requests
import datetime


class MtaTransit(object):

    def __init__(self):
        self.endpoint = "http://web.mta.info/status/serviceStatus.txt"
        self.data = self._get_data()
        self.scores = self._calculate_score()

    def _get_data(self):
        raw_xml_data = requests.get(self.endpoint).text
        data = xmltodict.parse(raw_xml_data, dict_constructor=dict)
        response_code = data['service']['responsecode']

        if int(response_code) == 0:
            payload = {
                'Subway': self._parse_transit(data['service']['subway']),
                'Bus': self._parse_transit(data['service']['bus']),
                'Bridges/Tunnels': self._parse_transit(data['service']['BT']),
                'LIRR': self._parse_transit(data['service']['LIRR']),
                'MetroNorth': self._parse_transit(data['service']['MetroNorth']),
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

    def _calculate_score(self):

        total_scores = {
            "DELAYS": 0,
            "GOOD SERVICE": 0,
            "PLANNED WORK": 0,
            "SERVICE CHANGE": 0,
            "OTHER": 0
        }

        # Count up statuses
        total_service_scores = {}
        for service, data in self.data.items():
            service_scores = {
                "DELAYS": 0,
                "GOOD SERVICE": 0,
                "PLANNED WORK": 0,
                "SERVICE CHANGE": 0,
                "OTHER": 0
            }
            if not isinstance(data, dict):
                continue

            for line, line_data in data.items():
                status = line_data.get('status')
                if status in total_scores.keys():
                    total_scores[status] += 1
                    service_scores[status] += 1
                else:
                    total_scores['OTHER'] += 1
                    service_scores['OTHER'] += 1

            total_service_scores[service] = service_scores

        # Calculate total score
        score = int(sum([total_scores['DELAYS'], total_scores['PLANNED WORK'], total_scores['SERVICE CHANGE']]) * 100 / sum(total_scores.values()))
        payload = {
            'total': score,
            'lines': {},
        }

        # Calculate individual lines
        for service, scores in total_service_scores.items():
            payload['lines'][service] = int(sum([scores['DELAYS'], scores['PLANNED WORK'], scores['SERVICE CHANGE']]) * 100 / sum(scores.values()))

        return payload
