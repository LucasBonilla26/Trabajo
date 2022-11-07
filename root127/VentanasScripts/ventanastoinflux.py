# python 3.6
import time
import paho.mqtt.client as mqtt # import the client1
import json
import time
import datetime
from influxdb import InfluxDBClient



def on_message(client, userdata, message):
    print("in-message")
    data=json.loads(str(message.payload.decode("utf-8"))) #recogida mensaje

    if data['object'] != {}:
        doorState = int(True if data['object']['door'] == "open" else False)
        informacion = {
            'measurement': data['deviceName'],
            'fields':{'rssi': float(data['rxInfo'][0]['rssi']),
            'loRaSNR': float(data['rxInfo'][0]['loRaSNR']),
            'door':doorState,
            'humidity':float(data['object']['humidity']),
            'temperature':float(data['object']['temperature'])}
        }

    #estructura datos a introducir en influxdb
        json_body = []
        json_body.append(informacion)
        print(json_body)

        db_host = '10.253.247.18'
        db_port = 8086
        db_user = 'admin'
        db_pass = 'alwayssmarter'
        db_name = 'sensors'

        cliente  = InfluxDBClient(host=db_host, port=db_port, username=db_user, password=db_pass)
        cliente.switch_database(db_name)
        datoinside = cliente.write_points(json_body, time_precision='s')#inserción datos


#conexión a cliente mqtt
broker_address = "158.49.112.171"
broker_port = 1883
topic = "application/11/device/+/event/up"
client = mqtt.Client("Subscriptor_ejem3")
client.username_pw_set(username="persianas",password="opticalflow")
print("pre-on-message")
client.on_message = on_message
client.connect(broker_address)
client.subscribe(topic)
print("pre-loop")
client.loop_forever()

