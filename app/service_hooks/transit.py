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
        self.total_score = self._calculate_total_score()

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

            transit_payload[line] = status

        return transit_payload


    def _calculate_score(self):
        payload = {}
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

            for line, status in data.items():
                if status in service_scores.keys():
                    service_scores[status] += 1
                else:
                    service_scores['OTHER'] += 1

            payload[service] = service_scores
            payload[service]['TOTAL_SCORE'] = int(sum([
                (.70 * service_scores['DELAYS']),
                (.15 * service_scores['PLANNED WORK']),
                (.15 * service_scores['SERVICE CHANGE'])
            ]) * 100 / sum(service_scores.values()))

        return payload

    def _calculate_total_score(self):
        aggregated = {
                "DELAYS": 0,
                "GOOD SERVICE": 0,
                "PLANNED WORK": 0,
                "SERVICE CHANGE": 0,
                "OTHER": 0
            }
        for line, data in self.scores.items():
            for key, inst_count in data.items():
                if key not in aggregated.keys():
                    continue

                aggregated[key] += inst_count

        score = int(sum([
                (.70 * aggregated['DELAYS']),
                (.15 * aggregated['PLANNED WORK']),
                (.15 * aggregated['SERVICE CHANGE'])
            ]) * 100 / sum(aggregated.values()))

        return score
