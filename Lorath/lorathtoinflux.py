# python 3.6
import time
import paho.mqtt.client as mqtt # import the client1
import json
import time
import datetime
from influxdb import InfluxDBClient



def on_message(client, userdata, message):
    data=json.loads(str(message.payload.decode("utf-8"))) #recogida mensaje
    print(data)
#     informacion = {
#     			'measurement': data['deviceName'],
#     			'tags': {'gatewayID': data['rxInfo'][0]['gatewayID']},
#                    	'fields': 
#                    		{
# 		           	'rssi': float(data['rxInfo'][0]['rssi']), 
# 		           	'loRaSNR': float(data['rxInfo'][0]['loRaSNR']),
# 		           	'batteryVoltage':float(data['object']['batteryVoltage']),
# 		           	'sensorCO2':float(data['object']['targetTemperature'])
#                    		}
#                   }

# #estructura datos a introducir en influxdb
#     json_body = []
#     json_body.append(informacion)
#     print(json_body)
#     cliente = InfluxDBClient(host='158.49.112.127', port=8086) #conexión influxdb
#     cliente.switch_database('co2_lora')
#     datoinside = cliente.write_points(json_body, time_precision='s')#inserción datos
#     print(data)

#conexión a cliente mqtt
broker_address = "158.49.112.171"
broker_port = 1883
topic = "persianas/#"
client = mqtt.Client("Subscriptor_ejem4")
client.username_pw_set(username="persianas",password="opticalflow")
client.on_message = on_message
client.connect(broker_address)
client.subscribe(topic)
client.loop_forever()

