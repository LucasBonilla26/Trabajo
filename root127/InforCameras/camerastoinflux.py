import json
import time
import requests
import subprocess
from influxdb import InfluxDBClient

client = InfluxDBClient(host='10.253.247.18', port=8086)
client.switch_database('sensors')
aulas = {"1": "C1", "2" : "C3", "3" : "C4", "4": "C5", "5" : "C6", "6" : "C7", "7": "C9-bis", "8": "I-1", "9" : "I-5", "10": "T1", "11": "T3", "12": "O6", "13": "O7"}
headers = {
    'Content-type': 'application/json',
}
data = '{"username": "locationapiunex@quodus.ai", "password": "a887a2045f03ab0e02034933f6cb23f4523b5e2ff707d5e18d6eedee2207a152"}'

USERNAME = 'locationapiunex@quodus.ai'
PASSWORD = 'a887a2045f03ab0e02034933f6cb23f4523b5e2ff707d5e18d6eedee2207a152'
SAMPLE_INTERVAL = 600  # seconds
response = requests.post('https://unex.admin.quodus.ai/token/auth', headers=headers, data=data)
bearer= 'Bearer ' + response.json()['access_token']
headers = {'Authorization': bearer,
             'Content-Type': 'application/json'}

while True:
    data = requests.get('https://unex.admin.quodus.ai/api/location-raw-latest', headers=headers).json()
    for camera in data:
        json_body = []
        infor = {'measurement' : aulas[str(camera['location_id'])], 'fields': {"ocupacion" : float(camera['count']) } }
        json_body.append(infor)
        datoinside = client.write_points(json_body, time_precision='s')
    time.sleep(SAMPLE_INTERVAL)
