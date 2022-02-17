##########################################################################
# Control de acceso por NFC con capacidad para registrar 8000 usuarios.
# El sistema almacena los usuarios ingresados en una memoria EEPROM.
# Detector NFC PN532 de Adafruit por SPI.
# Memoria EEPROM 24LC256 por I2C.
# Microcontrolador RP2040 (Raspberry PICO)
# Programación: MicroPython.
# Autor: Firtec Argentina
# Consultas: consultas@firtec.com.ar 
############################################################################
#NOTA: El ejemplo se ha ajustado para manejar solo 100 de los 8000 usuarios
#      posibles que se pueden almacenar en memoria.
############################################################################

from machine import Pin, Timer, I2C  # Importa las bibliotecas necesarias
import NFC_PN532 as nfc
from machine import Pin, SPI
import time
import utime

led = Pin(25, machine.Pin.OUT, machine.Pin.PULL_DOWN)
led.value(0)
beep = Pin(17, machine.Pin.OUT)
beep.value(0)
boton_Prog = Pin(15, Pin.IN, Pin.PULL_UP) # Boton programar TAG
boton_Borrar = Pin(14, Pin.IN, Pin.PULL_UP) # Boton borrar
#----- I2C para la memoria 24LC256 ----------
sda = machine.Pin(0)  
scl = machine.Pin(1) 
#------ Configura el puerto I2C -------------
I2C_BUS = machine.I2C(0, sda=sda, scl=scl, freq=400000)
#-------- Configura SPI para la placa lectora de NFC PN532 ---------
spi_dev = SPI(1,baudrate=100000, sck = Pin(10, Pin.OUT), mosi = Pin(11, Pin.OUT),miso = Pin(12, Pin.OUT))
cs = Pin(16, Pin.OUT)
cs.on()
# Detecta la placa PN532
pn532 = nfc.PN532(spi_dev,cs)
ic, ver, rev, support = pn532.get_firmware_version()
print('Encontrado PN532 con firmware version: {0}.{1}'.format(ver, rev))
# Configura las comunicaciones con PN532
pn532.SAM_configuration()

#----- Variables del programa ------
bandera_borrando = 0
error_usuario = 0
inicio = b'\x7f\xfe' # Aquí se almacena la dirección de memoria de los usuarios
#------------------------------------------------------
def scan_usuario(ID):
    global error_usuario
    pass
    for a in range(0,80):  # Recorre la memoria
            usuario_registrado = (I2C_BUS.readfrom_mem(80, a, 4, addrsize=16))
            usuario_registrado = usuario_registrado[:4]
            time.sleep_ms(20)
            if (usuario_registrado == ID):
                error_usuario = 1
                print('Encontrado el Usuario!!')
                print(ID)
                print('Dirección de memoria:',a)
                usuario_registrado = 0
                break
#-------------------------------------------------------
def borrar_memoria():
    global inicio
    bandera_borrando = 1
    print('Borrando...')
    for i in range(0,400):
        time.sleep_ms(20)
        beep.value(0)
        I2C_BUS.writeto_mem(80, i, b'\xFF', addrsize=16)
    print('Memoria Borrada!!')
    time.sleep_ms(10)
    a0 = int.from_bytes(inicio,"big")
    I2C_BUS.writeto_mem(80, a0, b'\x00\x00', addrsize=16)
    time.sleep_ms(20)
    add = 0
#-------------------------------------------------------
def prog_usuario(dev, tmot):
    global error_usuario
    global add
    global inicio
    add = 0
    a = 0
    a1 = 0
    nuevo_usuario = dev.read_passive_target(timeout=tmot)
    if nuevo_usuario is None:
        pass
        #print('PN532 NO ENCONTRADO!!')
    else:
        nuevo_ID = (nuevo_usuario) 
        nuevo_ID = nuevo_ID[:4] # Toma solo cuatro bytes del TAG
        print('Buscando...')
        scan_usuario(nuevo_ID)
          
        if (error_usuario == 0):
            print('Nuevo usuario: ', nuevo_ID)
            b0 = int.from_bytes(inicio,"big")
            
            a0 = I2C_BUS.readfrom_mem(80, b0, 2, addrsize=16)
            time.sleep_ms(10)
            a0 = int.from_bytes(a0, "big")
            I2C_BUS.writeto_mem(80, a0, nuevo_ID, addrsize=16) 
            time.sleep_ms(10)
            nuevo_ID = 0

            add = I2C_BUS.readfrom_mem(80, b0, 2, addrsize=16) # Recupera Dir. de memoria
            time.sleep_ms(20)
            a1 = int.from_bytes(add,"big") +4 # Pasa a entero e incrementa en 4 (son 4 bytes)
            add = (a1.to_bytes(len(add),'big')) # Pasa nuevamente a byte
            I2C_BUS.writeto_mem(80, b0, add, addrsize=16) # Guarda la nueva dir de memoria
            time.sleep_ms(20)
            if(add == b'\x00\x5f'):
                print('LA MEMORIA ESTA COMPLETA!!') 
                pass  #<<<<<< Definir accion
        error_usuario = 0    

def leer_usuario(dev, tmot):
    global error_usuario
    global inicio
    
    usuario = dev.read_passive_target(timeout=tmot)
    #usuario = [i for i in nuevo_usuario]
    if usuario is None:
        pass
        #print('PN532 NO ENCONTRADO!!')
    else:
        usuario = usuario[:4]
        scan_usuario(usuario)
        if(error_usuario == 1):
            beep.value(1)
            time.sleep_ms(200)
            beep.value(0)
            error_usuario = 0

while(1):
    if (boton_Prog.value() == 0):# and bandera_borrando == 0):
        prog_usuario(pn532, 500)
    if (boton_Borrar.value() == 0):
        borrar_memoria()
    leer_usuario(pn532, 500)
    pass
    beep.value(0)
    time.sleep_ms(100)
