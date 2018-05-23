import datetime
import flask
import requests
import psutil
import json
import time
from random import randint
from multiprocessing import Process


def get_stas_from_machine():
    ram = psutil.virtual_memory().used
    storage = psutil.disk_usage("/").used
    cpu = psutil.cpu_times_percent(1).system
    packets_sent = psutil.net_io_counters().packets_sent
    packets_received = psutil.net_io_counters().packets_recv
    packets_error = psutil.net_io_counters().errin + psutil.net_io_counters().errout

    return {
        'ram': ram,
        'storage': storage,
        'cpu': cpu,
        'packets':
            {
                'sent': packets_sent,
                'received': packets_received,
                'error': packets_error
            }
    }


class MyAction:
    __urad_url = "http://data.uradmonitor.com/api/v1/devices"
    __urad_headers = {'X-User-id': '4126', 'X-User-hash': '063cf4fdf721e844980c6f3b8b6eddcf'}

    __live_objects_url = "https://liveobjects.orange-business.com/api/v0/data/streams/tema5t5"
    __live_objects_headers = {'X-API-KEY': 'c80b688d6cfa4b238bf5b57416336261'}

    __request_loop_time = 7

    def get_data_from_devices(self):
        response = requests.get(url=self.__urad_url, headers=self.__urad_headers)

        return response.json()

    def from_urad_to_live_objects_format(self, obj):
        provider = 'URAD'
        source = 'urn:tenantName:FFFFFFFFFFFFFFFF!mystream'
        accuracy = 10

        response = {
            'location': {
                'accuracy': accuracy,
                'alt': obj['altitude'],
                'lat': obj['latitude'],
                'lon': obj['longitude'],
                'provider': provider
            },
            'metadata': {
                'source': source
            },
            'model': obj['detector'],
            'tags': [
                "Radiation",
                "Detector",
                "Temperature"
            ],
            'timestamp': str(datetime.datetime.now().isoformat())+"Z",
            'value': {
                'avg_temperature': obj['avg_temperature'],
                'avg_pressure': obj['avg_pressure'],
                'avg_humidity': obj['avg_humidity'],
                'avg_voc': obj['avg_voc'],
                'min_voc': obj['min_voc']
            }
        }

        print(json.dumps(response))

        return response

    def post_to_live_objects(self):
        while True:
            time.sleep(self.__request_loop_time)
            data = self.get_data_from_devices()
            print('Sending from urad to live objects')
            for obj in data:
                    data_to_be_sent = self.from_urad_to_live_objects_format(obj)
                    requests.post(self.__live_objects_url, headers=self.__live_objects_headers, json=data_to_be_sent)

    def get_data_from_live_objects(self):
        response = requests.get(self.__live_objects_url, headers=self.__live_objects_headers)
        return response


app = flask.Flask("aa")

from flask_cors import CORS, cross_origin

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

action = MyAction()


@app.route("/devices", methods=['GET'])
@cross_origin()
def devices():
    return json.dumps((action.get_data_from_live_objects().json()))


@app.route("/system/stats", methods=['GET'])
@cross_origin()
def system_stats():
    return json.dumps(get_stas_from_machine())


if __name__ == "__main__":
    Process(target=action.post_to_live_objects).start()
    app.run(host="127.0.0.1", debug=True)
