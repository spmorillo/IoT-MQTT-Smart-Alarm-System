# simple_device.py

#Librerias
from My_States import Apagado
from time import clock
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import MFRC522 # miso9 mosi10 sck11 sda8 rst25
import signal
import paho.mqtt.client as mqtt
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import pygame

#Teclado y pantalla
lcd_rs        = 7
lcd_en        = 21
lcd_d4        = 20
lcd_d5        = 16
lcd_d6        = 12
lcd_d7        = 26
lcd_backlight = 4
lcd_columns = 16
lcd_rows    = 2
MATRIX = [ [1,2,3],
	   [4,5,6],
	   [7,8,9],
	   ['*',0,'#'] ]

ROW = [4,17,27,22]
COL = [18,23,24] 

#Codigo
codigo = ['*','*','*','*']
indice_codigo = 0

#Objetos
MIFAREReader = 0
client = 0

#Flags
codigo_correcto = 0
codigo_erroneo = 0
alarma = 0

#temporizadores
start_desactivar_alarma = 0

#IP del MQTT
ip = "192.168.43.31"

#gmail
fromaddr = "sergipm11@gmail.com"
toaddr = "jaime.perez.sanchez@gmail.com"

#leds
led_verde = 13
led_rojo = 6

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
    setup_pantalla()
    setup_RFID()
    setup_MQTT()
    setup_camara()
    setup_leds()
    setup_audio()
    mensaje_inicial()
    
def setup_pantalla():
    global lcd
    lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,lcd_columns, lcd_rows, lcd_backlight)
    for j in range(3):
    	GPIO.setup(COL[j], GPIO.OUT)
    	GPIO.output(COL[j], 1)
    for i in range(4):
    	GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
        
def mensaje_inicial():
        lcd.clear()
        lcd.message('Bienvenido!')
        pygame.mixer.music.play()
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(6, GPIO.HIGH)
        delay(1)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        delay(1)
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(6, GPIO.HIGH)
        delay(1)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        print_introduce_el_codigo()
        
def setup_RFID():
    global MIFAREReader
    MIFAREReader = MFRC522.MFRC522()
          
def setup_camara():
    os.system("sudo service motion stop")
    os.system("sudo rm /home/pi/Desktop/motion/*")
    os.system("sudo rm video.zip")
    
def setup_leds():
    global led_verde, led_rojo
    GPIO.setup(led_verde, GPIO.OUT)
    GPIO.setup(led_rojo, GPIO.OUT)
    
def setup_audio():
    pygame.mixer.init()
    pygame.mixer.music.load("correct_code.mp3")
    pygame.mixer.music.load("error.mp3")
    pygame.mixer.music.load("Siren.mp3")
    pygame.mixer.music.load("welcome.mp3")

def setup_MQTT():    
    global client, ip
    client = mqtt.Client()
    client.connect(ip,1883,60) #puede cambiar la ip
    client.on_connect = on_connect
    client.on_message = on_message

"""
Funciones de entrada
"""

def transiciones_de_Apagado():
    Comprobar_codigo()
    Comprobar_RFID()

def transiciones_de_Encendido():
    Comprobar_codigo()
    Comprobar_RFID()
    
def transiciones_de_Activado():
    Comprobar_codigo()
    Comprobar_RFID()
    temporizador_alarma()
      
def Comprobar_codigo():
    global indice_codigo, codigo_correcto, codigo, codigo_erroneo, alarma
    if (indice_codigo == 4):
        if (codigo[0]==1 and codigo[1]==1 and codigo[2]==1 and codigo[3]==1):
            codigo_correcto = 1
        else:
            codigo_erroneo = 1       
            

#llavero = 156 193 40 131
#tarjeta = 211 154 172 28
def Comprobar_RFID():
    global MIFAREReader, codigo_correcto, codigo_erroneo
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
        (status,uid) = MIFAREReader.MFRC522_Anticoll()
        if status == MIFAREReader.MI_OK:
            if(uid[0] == 156 and uid[1] == 193 and uid[2] == 40 and uid[3] == 131):
                codigo_correcto = 1
            elif(uid[0] == 211 and uid[1] == 154 and uid[2] == 172 and uid[3] == 28):
                codigo_correcto = 1
            else:
                codigo_erroneo = 1
            
#No hace falta meterla en las transiciones ya que se activa sola            
def on_message(client, userdata, msg):
    global alarma
    print(msg.payload)
    if (msg.payload == b'puerta abierta'):
      alarma = 1 #meter mensaje personalizado
    if (msg.payload == b'distancia detectada'):
      alarma = 1
    if (msg.payload == b'presencia detectada'):
      alarma = 1

def temporizador_alarma():
    global codigo_correcto, start_desactivar_alarma
    if (time.time() > start_desactivar_alarma + 1800):
        if(start_desactivar_alarma != 0):
            codigo_correcto=1

"""
Funciones de Salida
"""

def alarma_activada():
    global codigo, indice_codigo, client
    borrar_flags()
    indice_codigo = 0
    codigo = ['*','*','*','*']
    lcd.clear()
    lcd.message('Correcto\n')
    pygame.mixer.music.load("correct_code.mp3")
    pygame.mixer.music.play()
    GPIO.output(13, GPIO.HIGH)
    setup_MQTT()
    client.loop_start()
    delay(1)
    lcd.clear()
    lcd.message('Activado\n')
    lcd.message('en 3 segundos')
    delay(3)
    GPIO.output(13, GPIO.LOW)
    print_introduce_el_codigo()
    
    
    
    
def alarma_desactivada():
    global codigo, indice_codigo, client, start_desactivar_alarma
    borrar_flags()
    indice_codigo = 0
    codigo = ['*','*','*','*']
    start_desactivar_alarma = 0
    pygame.mixer.music.stop()
    lcd.clear()
    lcd.message('Correcto\n')
    pygame.mixer.music.load("correct_code.mp3")
    pygame.mixer.music.play()
    GPIO.output(13, GPIO.HIGH)
    client.loop_stop()
    client.disconnect()
    os.system("sudo service motion stop")
    if(device.state.__repr__() == 'Activado'):
        enviar_mail()
    delay(1)
    lcd.clear()
    lcd.message('Desactivado\n')
    lcd.message('en 3 segundos')
    delay(3)
    GPIO.output(13, GPIO.LOW)
    print_introduce_el_codigo()
    
    
def codigo_fallado():
    global codigo, indice_codigo , client
    borrar_flags()
    indice_codigo = 0
    codigo = ['*','*','*','*']
    lcd.clear()
    lcd.message('Error')
    pygame.mixer.music.load("error.mp3")
    pygame.mixer.music.play()
    GPIO.output(6, GPIO.HIGH)
    delay(3)
    GPIO.output(6, GPIO.LOW)
    print_introduce_el_codigo()
    
def sensor_activo():
    global start_desactivar_alarma
    borrar_flags()
    lcd.clear()
    lcd.message('ALARMA')
    pygame.mixer.music.load("Siren.mp3")
    pygame.mixer.music.play(loops=9999)
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    client.loop_stop()
    client.disconnect()
    os.system("curl -X POST https://maker.ifttt.com/trigger/alarma/with/key/kyGx64jHARP2RKhJFKEIV5SJcOtHR-pKjBBKeN65vHD")
    os.system("sudo service motion start")
    start_desactivar_alarma = time.time()
    delay(5)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    print_introduce_el_codigo()
       



"""
Otras funciones
"""


def teclado_y_pantalla():
    global indice_codigo, codigo
    try:
        for j in range(3):
            GPIO.output(COL[j],0)
            for i in range(4):
                if (GPIO.input(ROW[i]) == 0):
                    codigo[indice_codigo] = MATRIX[i][j]
                    indice_codigo=indice_codigo + 1
                    print_introduce_el_codigo()
                    while (GPIO.input(ROW[i]) == 0):
                        pass
            GPIO.output(COL[j],1)
    except KeyboardInterrupt:
        GPIO.cleanup()

def print_introduce_el_codigo():
    global codigo
    lcd.clear();
    lcd.message('Codigo:\n')
    for k in range(4):
        lcd.message(str(codigo[k]))

def delay(tiempo):
    start = clock()
    while(start + tiempo > clock()):
        pass       
        
def borrar_flags():
    global codigo_correcto, codigo_erroneo, alarma
    codigo_correcto = 0
    codigo_erroneo = 0
    alarma = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("puerta",2)
    client.subscribe("distancia", 2)
    client.subscribe("presencia", 2)

def enviar_mail():
    os.system("sudo zip -r video.zip /home/pi/Desktop/motion -j")
    
    if(os.path.isfile("video.zip")==True):
        msg = MIMEMultipart()
         
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Alerta de seguridad en tu hogar."
         
        body = "Buenos dias, la alarma se ha activado, revise el video adjunto."
         
        msg.attach(MIMEText(body, 'plain'))
         
        filename = "video.zip"
        attachment = open("video.zip", "rb")
         
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
         
        msg.attach(part)
         
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "xxx") #introducir contraseña
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
    
    os.system("sudo mv /home/pi/Desktop/motion/* /home/pi/Desktop/videos_antiguos/")
    os.system("sudo rm video.zip")
    
#Para que no muera la raspi
def end_read(signal,frame):
    print ("Ctrl+C captured, ending read.")
    GPIO.cleanup()

signal.signal(signal.SIGINT, end_read)    

 
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
                device.on_event('Encendido')
            elif (codigo_erroneo == 1):
                codigo_fallado()
        elif (device.state.__repr__() == 'Encendido'):
            transiciones_de_Encendido()
            if (codigo_correcto == 1):
                alarma_desactivada()
                device.on_event('Apagado')
            elif(codigo_erroneo == 1):
                codigo_fallado()
            elif(alarma==1):
                sensor_activo()
                device.on_event('Activado')
        elif (device.state.__repr__() == 'Activado'):
            transiciones_de_Encendido()
            if (codigo_correcto == 1):
                alarma_desactivada()
                device.on_event('Apagado')
            elif(codigo_erroneo == 1):
                codigo_fallado()
        #Delay de la maquina de estados
        delay(0.0005)