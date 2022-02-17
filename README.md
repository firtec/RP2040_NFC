Lectura de NFC mediante RP2040 (Raspberry Pico)
El siguiente ejemplo lee los  TAG NFC mediante el chip PN532 monstado en una placa de  Adafruit mediante bus SPI.
El contrlador usado es el RP2040 montado a bordo de una placa Raspberry Pico, los usuarios son almacenados en una memoria I2C 24LC256.
El ejemplo podría administra 8000 usuarios pero se ha  dispuesto que solo se manejen 100 para agili el borrado y búsqueda en memoria.
La programación es MicroPython.
Dos boton conectads en los pines GP14_15 se encargan de manejar el borrado de la memoria como  también la programación de nuevos usuarios

aUTOR: FIRTEC ARGENTINA
