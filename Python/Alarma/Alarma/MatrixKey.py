import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
lcd_rs        = 7
lcd_en        = 21
lcd_d4        = 20
lcd_d5        = 16
lcd_d6        = 12
lcd_d7        = 26
lcd_backlight = 4
lcd_columns = 16
lcd_rows    = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,lcd_columns, lcd_rows, lcd_backlight)
#GPIO.setmode(GPIO.BOARD)
MATRIX = [ [1,2,3],
	   [4,5,6],
	   [7,8,9],
	   ['*',0,'#'] ]

ROW = [4,17,27,22]
COL = [18,23,24] 
aux=0
for j in range(3):
	GPIO.setup(COL[j], GPIO.OUT)
	GPIO.output(COL[j], 1)

for i in range(4):
	GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

try:
	while(True):		
		for j in range(3):
			GPIO.output(COL[j],0)

			for i in range(4):
				if GPIO.input(ROW[i]) == 0:
					print (MATRIX[i][j])
					lcd.message(str(MATRIX[i][j]))
					aux=aux+1
					if aux == 17:
						aux=0
						lcd.clear()
					while (GPIO.input(ROW[i]) == 0):
						pass
			GPIO.output(COL[j],1)
except KeyboardInterrupt:
	GPIO.cleanup()
