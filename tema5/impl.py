import requests
import psutil
import os
import time

def get_data_from_devices():

    url = "http://data.uradmonitor.com/api/v1/devices"
    headers = {'X-User-id':'4126','X-User-hash':'063cf4fdf721e844980c6f3b8b6eddcf'}
    response = requests.get(url=url,headers=headers)

    return response

#pachete trimise
#receptionate si erori

print(psutil.net_io_counters().packets_sent)
print(psutil.net_io_counters().packets_recv)
print(psutil.net_io_counters().errin + psutil.net_io_counters().errout)
