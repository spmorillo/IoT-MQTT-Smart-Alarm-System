import time
import picamera
import os

camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.start_preview()

camera.start_recording('tmp.h264')
time.sleep(10)
os.system("sudo service motion start")
camera.stop_recording()
camera.stop_preview()