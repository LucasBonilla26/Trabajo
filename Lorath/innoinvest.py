from influxdb import InfluxDBClient
import json
import requests
from requests.structures import CaseInsensitiveDict
client = InfluxDBClient(host='10.253.247.18', port=8086)
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


url = "https://innoinvest.elliotcloud.com:443/api/v1/input/json"
headers = CaseInsensitiveDict()
headers["Authorization"] ="Basic YWRtaW46aW5ub2ludmVzdF9qZTIwMjI="
headers["Content-Type"] = "application/json"
client.switch_database('sensors')
measurements = client.get_list_measurements()
print(measurements)
sensors = []
dict_time={}
for a in measurements:
    for valor in a.values():
        if valor[0:2] == "UE":
            sensors.append(valor)
            dict_time[valor] = "nothing"


while True:
    for x in sensors:
        fecha = 0
        # string =  SELECT last(value) FROM response_times WHERE time > now() - 1
        string = 'SELECT * FROM %s WHERE time > now() - 1h GROUP BY * ORDER BY DESC LIMIT 1 ' % x
        #string = 'SELECT * FROM %s GROUP BY * ORDER BY DESC LIMIT 1 ' % x
        # string = 'SELECT * FROM %s GROUP BY * ORDER BY DESC LIMIT 1' % sensors[5]
        queryraw = client.query(string).raw
        data_dict = {}
        if len(queryraw["series"]) > 0:
            for a in range(0, len(queryraw['series'][0]['columns'])):
                if a == 0:
                    fecha = queryraw['series'][0]['values'][0][a]
                else:
                    data_dict[queryraw['series'][0]['columns'][a]] = str(queryraw['series'][0]['values'][0][a]).replace(",", "")
            data = [data_dict]
            data_json = {"info": {"api_key": "000000", "device": x}, "data": data}
            json_str = json.dumps(data_json).replace(" ", "")
            if dict_time[x] != fecha:
                resp = requests.post(url, headers=headers, data=json_str)
                print(json_str)
                dict_time[x] = fecha
            else:
                pass
