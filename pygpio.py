# A Semi decent GPIO lbrary for python3 made by Jeremiah Lowe (aka abc123me)
# Usage instructions:
# 1: Import the library using 'import pygpio'
# 2: Initialize your GPIOPin using 'pin = pygpio.GPIOPin(pinNumber)'
# 3: Set the mode of your GPIOPin using 'pin.setMode(True) for output or pin.setMode(False) for input'
# 4: Read and write to the pin as much as you want (Keep in mind you can't write to input pins!)

import sys
if(sys.version_info[0] < 3): #Check python version
    raise "This only supports python3!"

from subprocess import call
from os.path import isfile
from os.path import isdir
import colors


#A GPIOError class for making debugging of GPIO related errors alot easier
class GPIOError(Exception): #Base class for handling GPIO related errors
    def __init__(self, pin, step, message):
        self.pin = pin
        self.step = step
        self.message = message
    def __str__(self):
        return "GPIO Error during " + self.step + " step! Caused by: " + self.message



def fwrite(file, toWrite):
    f = open(file, "w")
    f.write(str(toWrite))


#A GPIOPin class for declaring GPIO pins
class GPIOPin:
    def __init__(self, pin): #Constructor called when object is created, takes in the pin number for the specified gpio pin
        self.pinID = pin
        self.exported = False
        self.pinStr = ""
        self.isOutput = False
        self.valueFile = None
        self.isNegated = False
        if(not isfile("/sys/class/gpio/export")):
            raise GPIOError(self, "init", "GPIO is unsupported on your system! (/sys/class/gpio/export don't exist)")
        if(not isfile("/sys/class/gpio/unexport")):
            raise GPIOError(self, "init", "GPIO is unsupported on your system! (/sys/class/gpio/unexport don't exist)")
    def __str__(self):
        return "GPIO pin " + str(self.pinID)

    #Export and unexport subroutines handled by setMode and destructor, not the end user
    #Exports the pin
    def export(self):
        fwrite("/sys/class/gpio/export", self.pinID)
        self.pinStr = "/sys/class/gpio/gpio" + str(self.pinID)
        if(not self.checkExport()):
            raise GPIOError(self, "export", "Failed to export GPIO pin: " + self.pinStr)
    #Unexports the pin
    def unexport(self):
        fwrite("/sys/class/gpio/unexport", self.pinID)
        if(self.checkExport()):
            raise GPIOError(self, "unexport", "Failed to unexport GPIO pin: " + self.pinStr)
    #Checks if pin is exported
    def checkExport(self):
        exp = isdir(self.pinStr)
        self.exported = exp;
        return exp;

    #Sets the mode of the GPIO pin, should be handled by the end user first
    def setMode(self, isOutput):
        mode = "in"
        if(isOutput):
            mode = "out"
        if(not self.checkExport()):
            self.export()
        pinf = self.pinStr + "/direction"
        if(not isfile(pinf)):
            raise GPIOError(self, "setMode", "Unable to set " + pinf + " to " + self.mode)
        fwrite(pinf, mode)
        if(isOutput):
            self.valueFile = open(self.pinStr + "/value", "w")
        else:
            self.valueFile = open(self.pinStr + "/value", "r")
        self.mode = mode
        self.isOutput = isOutput
    #Cool extensions methods for setMode
    def setInput(self):
        self.setMode(False)
    def setOutput(self):
        self.setMode(True)

    #Reading and writing to pins, should be handled by end user
    #Write a value to the specified GPIO pin
    def write(self, val):
        if(self.isNegated):
            val = not val
        w = "0"
        if(val):
            w = "1"
        if(not self.exported):
            raise GPIOError(self, "write", "Pin not exported, export with setMode(mode) or export()")
        if(not self.isOutput):
            raise GPIOError(self, "write", "Cannot write to input pin, set mode with setMode(mode)!")
        fwrite(self.pinStr + "/value", w)
    #Read the value of a specified GPIO pin
    def digitalRead(self):
        if(not self.exported):
            raise GPIOError(self, "read", "Pin not exported, export with setMode(mode) or export()")
        if(self.isOutput):
            raise GPIOError(self, "read", "Cannot read from output pin, set mode with setMode(mode)!")
        self.valueFile.seek(0)
        out = self.valueFile.read()
        val = int(out)
        if(self.isNegated):
            return not(val > 0)
        else:
            return (val > 0)

#A EMULATED GPIOPin class for declaring GPIO pins but emulating them (aka theyre not real pins)
class EmulatedGPIOPin:
    def __init__(self, pin, isNegated): #Constructor called when object is created, takes in the pin number for the specified gpio pin
        self.pinID = pin
        self.exported = False
        self.isOutput = False
        self.isNegated = False
        from random import randint
    def __str__(self):
        return "Emulated GPIO pin " + str(self.pinID)

    #Export and unexport subroutines handled by setMode and destructor, not the end user
    #Exports the pin
    def export(self):
        self.exported = True
    #Unexports the pin
    def unexport(self):
        self.exported = False
    #Checks if pin is exported
    def checkExport(self):
        return self.exported;

    #Sets the mode of the GPIO pin, should be handled by end user first
    def setMode(self, isOutput):
        mode = "in"
        if(isOutput):
            mode = "out"
        if(not self.checkExport()):
            self.export()
        val = colors.magenta + "input"
        if(isOutput):
            val = colors.yellow + "output"
        val = val + colors.cyan
        print(colors.cyan + "Set GPIO pin " + str(self.pinID) + " to " + val + "!" + colors.reset)
        self.mode = mode
        self.isOutput = isOutput
    #Cool extensions methods for setMode
    def setInput(self):
        self.setMode(False)
    def setOutput(self):
        self.setMode(True)

    #Reading and writing to pins, should be handled by end user
    #Write a value to the specified GPIO pin
    def write(self, val):
        if(not self.exported):
            raise GPIOError(self, "write", "Pin not exported, export with setMode(mode) or export()")
        if(not self.isOutput):
            raise GPIOError(self, "write", "Cannot write to input pin, set mode with setMode(mode)!")
        if(self.isNegated):
            val = not val
        if(val):
            print(colors.cyan + "Set GPIO " + str(self.pinID) + " to " + colors.green + "HIGH" + colors.reset)
        else:
            print(colors.cyan + "Set GPIO " + str(self.pinID) + " to " + colors.red + "LOW" + colors.reset)
    #Read the value of a specified GPIO pin
    def digitalRead(self):
        if(not self.exported):
            raise GPIOError(self, "read", "Pin not exported, export with setMode(mode) or export()")
        if(self.isOutput):
            raise GPIOError(self, "read", "Cannot read from output pin, set mode with setMode(mode)!")
        return (randint(0, 100) > 50)
