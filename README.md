# Main
## Debugging
When adding the following to the top of main.py it will put everything in a "debug" mode where all status pins are ignored and no GPIO pins are actually set
``` python
#IMPORTANT: COMMENT EVERYTHING FROM HERE OUT if you are testing/running the code on the real thing
import iol
iol.MAKE_EMULATED()           #Sets all GPIO pins, and Baseball switch to emulated mode
EMULATING_TRANSLATOR = True   #Modifies the isTranslatorOn to return the correct value every time (ignoring status pins)
EMULATING_NOISE_SOURCE = True #Modifies the isNoiseSourceOn to return the correct value every time (ignoring status pins)
#TO HERE
```
# iol Package (and asc. libraries)
The iol package stands for <u>I</u>nput <u>O</u>utput <u>L</u>ibraries (iol), meaning it is the single codebase for ALL of the input/output related code, it currently includes the libraries for reading from the ADC, Baseball switches, and GPIO pins
## iol.pygpio
For GPIO use pygpio since it is currently working and is simple to use, heres some example code:
``` python
from iol.pygpio import GPIOPin           #Imports the pygpio.py file, make sure it is in the same directory as your script!
pin = GPIOPin(INTEGER_PIN_NUMBER)        #Initializes the GPIO pin
pin.setMode(BOOLEAN_IS_OUTPUT)           #Sets the mode of the GPIO pin, False for input, True for output
pin.write(BOOLEAN_VALUE)                 #Only works for output pins
pin.digitalRead()                        #Only works for input pins
```
Also, The GPIO library requires superuser privledges so use sudo or run as root (or creating a gpio group and adding the user to that)
An example led blink script `blink_example.py` was created to demonstrate how to use the GPIO library

As an extension of the GPIO library I created the Baseball library for controlling the three baseball switches that are nescessary, this will deal with preventing the positions from becoming locked, also in no way can a software bug cause the switch to not activated due to the redundancy added by first setting both of the position pins to LOW then bringing the required pin to HIGH
## iol.baseball
``` python
from iol.baseball import BaseballSwitch
setAPin = 9                              #A position indicator
setBPin = 10                             #B position indicator
posAPin = 11                             #Output pin to control the A coil
posBPin = 12                             #Output pin to control the B coil
baseball = BaseballSwitch("The switches name used for debugging", setAPin, setBPin, posAPin, posBPin) #Initialize the switch

baseball.initGPIO() # This initializes the GPIO pins of the switch (using iol.pygpio)

baseball.setPosition("a")                #Puts the switch in the A position
baseball.setPosition(True)               #Puts the switch in the A position
baseball.setPosition("b")                #Puts the switch in the B position
baseball.setPosition(False)              #Puts the switch in the B position
baseball.swapPos()                       #This will swap it's position
baseball.getPosition()                   #Gets the position (returns an "a" or "b")
baseball.reset()                         #Resets both setting pins to False
baseball.setSwitchingDelay(time)         #Sets the switching delay
baseball.getDelay()                      #Gets the switching delay in seconds   
```
