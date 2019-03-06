from gpiozero import Buzzer
import time

buzzer = Buzzer(6)
startTime = time.time()
buzzer.on()
buzzer.beep()
while(True):
    if (time.time() > startTime + 3):
        buzzer.off()
