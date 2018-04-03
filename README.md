# nasa_dsn
NASA Deep space network stuff

For GPIO use pygpio since it is currently working and is simple to use, heres some example code:
``` python
import pygpio
pin = pygpio.GPIOPin(INTEGER_PIN_NUMBER)
pin.setMode(BOOLEAN_IS_OUTPUT)
pin.write(BOOLEAN_VALUE) #Only works for output pins
pin.read() #Only works for input pins
```

