# nasa_dsn
NASA Deep space network stuff

## GPIO
For GPIO use pygpio since it is currently working and is simple to use, heres some example code:
``` python
import pygpio                            #Imports the pygpio.py file, make sure it is in the same directory as your script!
pin = pygpio.GPIOPin(INTEGER_PIN_NUMBER) #Initializes the GPIO pin
pin.setMode(BOOLEAN_IS_OUTPUT)           #Sets the mode of the GPIO pin, False for input, True for output
pin.write(BOOLEAN_VALUE)                 #Only works for output pins
pin.read()                               #Only works for input pins
```
Also, The GPIO library requires superuser privledges so use sudo or run as root (or creating a gpio group and adding the user to that)
An example led blink script `blink_example.py` was created to demonstrate how to use the GPIO library
