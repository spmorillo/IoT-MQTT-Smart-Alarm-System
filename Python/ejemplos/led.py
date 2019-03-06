import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
time.sleep(2)
GPIO.output(13, GPIO.HIGH)
startTime = time.time()
while(True):
    if (time.time() > startTime + 3):
        GPIO.output(13, GPIO.LOW)
