import pygpio
from time import sleep

pin = pygpio.GPIOPin(0)
pin.setMode(True)

val = True

while True:
	val = not val
	pin.write(val)
	sleep(0.5)
