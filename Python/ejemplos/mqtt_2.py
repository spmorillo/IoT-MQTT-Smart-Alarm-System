import paho.mqtt.publish as publish
#import time

#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time

#topic: puerta       payload: puerta abierta
#topic: distancia    payload: distancia detectada 
#topic: presencia    payload: presencia detectada

i = 0


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("puerta")
    client.subscribe("presencia")
    client.subscribe("distancia")

def on_message(client, userdata, msg):
    global i
    print(msg.payload)
    if (msg.payload == b'presencia detectada'):
      i=i+1
      print('Alarma activada! ' + str(i))
      time.sleep(5)

client = mqtt.Client()
client.connect("192.168.43.31",1883,60)

client.on_connect = on_connect
client.on_message = on_message


client.loop_start()
