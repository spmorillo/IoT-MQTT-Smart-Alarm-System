import picamera
import time

camera = picamera.PiCamera()
camera.resolution = (640, 480)

camera.start_preview()
time.sleep(10)
camera.stop_preview()