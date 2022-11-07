# python 3.6
import time
import paho.mqtt.client as mqtt # import the client1

broker_address = "158.49.112.190"
broker_port = 1883
topic = "application/1/device/+/event/up"

def on_message(client, userdata, message):
    print("Mensaje recibido=", str(message.payload.decode("utf-8")))
    print("Topic=", message.topic)
    print("Nivel de calidad [0|1|2]=", message.qos)
    print("Flag de retención o nuevo?=", message.retain)

client = mqtt.Client("Subscriptor_ejem1")
client.on_message = on_message
client.connect(broker_address)
#client.loop_start() # Inicio del bucle
client.subscribe(topic)
client.loop_forever()
#time.sleep(10) # Paramos el hilo para recibir mensajes.
#client.loop_stop() # Fin del bucle
