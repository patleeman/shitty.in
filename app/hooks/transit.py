"""
transit.py
MTA Service Status

Requests and parses the NYC MTA's service status.  Then calculates the shitty score.

"""

import xmltodict
import requests
import requests_cache



class MtaTransit(object):
    def __init__(self):
        self.payload = None

    def get_data(self):
        # Get data
        self.payload = {"breakdown": self._query_api()}

        # Calculate individual scores
        for line, data in self.payload['breakdown'].items():
            service_score = self._calculate_service_scores(data['status'])
            self.payload['breakdown'][line]['score'] = service_score

        # Calculate total score
        total_service_scores = {
            "DELAYS": 0,
            "GOOD SERVICE": 0,
            "PLANNED WORK": 0,
            "SERVICE CHANGE": 0,
            "OTHER": 0
        }
        for mot, data in self.payload['breakdown'].items():
            for line, status in data['status'].items():
                if status in total_service_scores.keys():
                    total_service_scores[status] += 1
                else:
                    total_service_scores['OTHER'] += 1


        self.payload['score'] = self._calculate_total_score(total_service_scores)
        return self.payload


    def _query_api(self):
        """
        Get data from MTA Service api endpoint.
        :return:
        """
        endpoint = "http://web.mta.info/status/serviceStatus.txt"
        requests_cache.install_cache('transit-cache', backend='sqlite', expire_after=180)
        raw_xml_data = requests.get(endpoint).text
        data = xmltodict.parse(raw_xml_data, dict_constructor=dict)
        response_code = data['service']['responsecode']

        if int(response_code) == 0:
            payload = {
                'Subway': {"name": "Subway", "status": self._parse_transit(data['service']['subway'])},
                'MTA Buses': {"name": "MTA Buses", "status": self._parse_transit(data['service']['bus'])},
                'Bridges & Tunnels': {"name": 'Bridges & Tunnels', "status": self._parse_transit(data['service']['BT'])},
                'LIRR': {"name": 'LIRR', "status": self._parse_transit(data['service']['LIRR'])},
                'Metro North': {"name": 'Metro North', "status": self._parse_transit(data['service']['MetroNorth'])},
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


    def _calculate_service_scores(self, data):
        """
        Takes object containing the current status of each individual service within
        each mode of transport.
        :param data:
        :return:
        """
        service_scores = {
            "DELAYS": 0,
            "GOOD SERVICE": 0,
            "PLANNED WORK": 0,
            "SERVICE CHANGE": 0,
            "OTHER": 0
        }

        for line, status in data.items():
            if status in service_scores.keys():
                service_scores[status] += 1
            else:
                service_scores['OTHER'] += 1

        total_score = self._calculate_total_score(service_scores)

        return total_score


    @staticmethod
    def _calculate_total_score(service_scores):
        total_score = int(sum([
            (.50 * service_scores['DELAYS']),
            (.20 * service_scores['PLANNED WORK']),
            (.30 * service_scores['SERVICE CHANGE'])
        ]) * 100 / sum(service_scores.values()))

        return total_score
