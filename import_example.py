import pygpio, sys
from time import sleep

pin = pygpio.GPIOPin(5)
pin.setMode(False)

while True: 
    if(pin.digitalRead()):
        print("ON")
    else:
        print("OFF")
    sleep(1)


