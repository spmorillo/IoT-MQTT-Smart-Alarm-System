# simple_device.py

from My_States import Apagado
from time import clock
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
#GPIO.setmode(GPIO.BOARD)
MATRIX = [ [1,2,3],
	   [4,5,6],
	   [7,8,9],
	   ['*',0,'#'] ]

ROW = [4,17,27,22]
COL = [18,23,24] 

codigo_correcto = 0
codigo = ['*','*','*','*']
indice_codigo =0


class SimpleDevice(object):
    """ 
    A simple state machine that mimics the functionality of a device from a 
    high level.
    """

    def __init__(self):

        self.state = Apagado()

    def on_event(self, event):
        """
        This is the bread and butter of the state machine. Incoming events are
        delegated to the given states which then handle the event. The result is
        then assigned as the new state.
        """

        # The next state will be the result of the on_event function.
        self.state = self.state.on_event(event)

"""
Funcioines de setup
"""        

def setup():
    setup_Matriz() 
    setup_pantalla()
        
def setup_Matriz():
    global lcd
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,lcd_columns, lcd_rows, lcd_backlight)
   
    for j in range(3):
    	GPIO.setup(COL[j], GPIO.OUT)
    	GPIO.output(COL[j], 1)
    
    for i in range(4):
    	GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
        
def setup_pantalla():
        lcd.clear()
        lcd.message('Bienvenido!')

"""
Funciones de entrada
"""

def transiciones_de_Apagado():
    Comprobar_codigo()

def transiciones_de_Encendido():
    Comprobar_codigo()
    
def transiciones_de_Activado():
    pass
      
def Comprobar_codigo():
    global indice_codigo, codigo_correcto, codigo
    if (indice_codigo == 4):
        indice_codigo = 0
        lcd.clear()
        if (codigo[0]==1 and codigo[1]==1 and codigo[2]==1 and codigo[3]==1):
            codigo_correcto = 1
        else:
             lcd.message('Try again!')
             delay_de_3s()     
        codigo = ['*','*','*','*']       
        # print('entro')
        


"""
Funciones de Salida
"""

def alarma_activada():
    global codigo_correcto
    codigo_correcto=0
    lcd.message('Activado:\n')
    lcd.message('en 3 segundos')
    delay_de_3s()
    device.on_event('pin_entered')
    
def alarma_desactivada():
    global codigo_correcto
    codigo_correcto=0
    lcd.message('Desactivado\n')
    lcd.message('en 3 segundos')
    delay_de_3s()
    device.on_event('device_locked')


"""
Otras funciones
"""


def teclado_y_pantalla():
    global indice_codigo
    try:
        for j in range(3):
            GPIO.output(COL[j],0)
            for i in range(4):
                if (GPIO.input(ROW[i]) == 0):
                    codigo[indice_codigo] = MATRIX[i][j]
                    indice_codigo=indice_codigo + 1
                    lcd.clear();
                    lcd.message('Introduzca el codigo\n')
                    for k in range(4):
                        lcd.message(str(codigo[k]))
                    while (GPIO.input(ROW[i]) == 0):
                        pass
            GPIO.output(COL[j],1)
    except KeyboardInterrupt:
    	GPIO.cleanup()
        
def delay_de_3s():
    time = 3
    start = clock()
    while(start + time > clock()):
        pass

       
        
def borrar_flags():
    pass
 
"""
Bucle principal
"""  
    
    
if __name__ == "__main__":
   
    device = SimpleDevice()
    setup()
 
    while(1):
        
        teclado_y_pantalla()
        
        if (device.state.__repr__() == 'Apagado'):          
            transiciones_de_Apagado()
            if (codigo_correcto == 1):
                alarma_activada()
        elif (device.state.__repr__() == 'Encendido'):          
            transiciones_de_Encendido()
            if (codigo_correcto == 1):
                alarma_desactivada()
                
                
        
        #Delay de la maquina de estados
        timerInterval = 1
        startTime = clock()
        while(startTime + timerInterval > clock()):
            pass