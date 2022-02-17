
from machine import Pin, Timer  # Importa las bibliotecas necesarias
import NFC_PN532 as nfc
from machine import Pin, SPI
import time
reset = Pin(15, machine.Pin.OUT, machine.Pin.PULL_DOWN)
reset.value(0)
beep = Pin(17, machine.Pin.OUT)
beep.value(0)
# SPI
spi_dev = SPI(1,baudrate=100000, sck = Pin(10, Pin.OUT), mosi = Pin(11, Pin.OUT),miso = Pin(12, Pin.OUT))
cs = Pin(16, Pin.OUT)
cs.on()

# SENSOR INIT
pn532 = nfc.PN532(spi_dev,cs)
ic, ver, rev, support = pn532.get_firmware_version()

print('Encontrado PN532 con firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()
dato_viejo = 0
# FUNCTION TO READ 
def read_nfc(dev, tmot):
    global dato_viejo
    
    """Accepts a device and a timeout in millisecs """
    #print('Buscando...')
    uid = dev.read_passive_target(timeout=tmot)
    if uid is None:
        pass
        #print('PN532 NO ENCONTRADO!!')
    else:
        dato = [i for i in uid]
    
        string_ID = '{}{}{}{}'.format(*dato)
        
        #print('Detectada tarjeta con UID:', [hex(i) for i in uid])
        if (string_ID != dato_viejo):
            dato_viejo = string_ID
            print('Detectado ID: {}'.format(string_ID))
            beep.value(1)
            time.sleep_ms(100)
while(1):
    
    read_nfc(pn532, 500)
    pass
    beep.value(0)
    #time.sleep_ms(1000)
