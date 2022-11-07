import json
import time
import requests
import subprocess

BASH = 'bash'
PATH_LOGIN = 'bash/api_login.sh'
PATH_AUTH = 'bash/api_auth.sh'

USERNAME = 'locationapiunex@quodus.ai'
PASSWORD = 'a887a2045f03ab0e02034933f6cb23f4523b5e2ff707d5e18d6eedee2207a152'
SAMPLE_INTERVAL = 600  # seconds

URL = 'http://158.49.112.127:11223/InsertDataInflux?json={"info":{"api_key":"000000","device":"location_id"},' \
      '"data":{"people":"counter"}}'
REPLACEABLE = ['location_id', 'counter']

LOGIN = subprocess.run([BASH, PATH_LOGIN, USERNAME, PASSWORD], capture_output=True, text=True)
STDOUT = LOGIN.stdout
AUTH = STDOUT[:len(STDOUT) - 1]  # delete line break

while True:
    responseJson = subprocess.run([BASH, PATH_AUTH, AUTH], capture_output=True, text=True)
    response = json.loads(responseJson.stdout)
    print(response)

    for camera in response:
        print(camera)
        camname = 'AULCAM' + str(camera.get('location_id'))
        urlComplete = URL.replace(REPLACEABLE[0], camname )\
        .replace(REPLACEABLE[1], str(camera.get('count')))
        requests.get(urlComplete)



    time.sleep(SAMPLE_INTERVAL)
