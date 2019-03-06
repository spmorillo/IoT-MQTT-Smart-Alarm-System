import paho.mqtt.publish as publish
import time

while(True):
   print("Sending 1...")
   publish.single("ledStatus", "1", hostname="192.168.43.31")
   time.sleep(6)
   print("Sending 0...")
   publish.single("ledStatus", "0", hostname="192.168.43.31")
   time.sleep(3)

