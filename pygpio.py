# A Semi decent GPIO lbrary for python3
import sys
if(sys.version_info[0] < 3): #Check python version
   raise "This only supports python3!"

from subprocess import call
from os.path import isfile
from os.path import isdir
class GPIOError(Exception): #Base class for handling GPIO related errors
   def __init__(self, pin, step, message):
      self.pin = pin
      self.step = step
      self.message = message
   def __str__(self):
      return "GPIO Error during " + self.step + " step! Caused by: " + self.message
   
class GPIOPin:
   def __init__(self, pin): #Constructor called when object is create
      self.pinID = pin
      self.exported = False
      self.pinStr = ""
      self.isOutput = False
   def __del__(self): #Deconstructer called when object is no longer used
      if(self.exported):
         self.unexport()
   def __str__(self):
      return "GPIO pin #" + pinID
   #Export and unexport subroutines handled by setMode and destructor
   #Exports the pin
   def export(self): 
      ef = "/sys/class/gpio/export"
      if(not isfile(ef)):
         raise GPIOError(self, "export", ef + " does not exist, Cannot export GPIO!")
      f = open(ef, "w")
      f.write(self.pinID)
      f.close()
      self.pinStr = "/sys/class/gpio" + self.pinID
      if(not isdir(self.pinStr)):
         raise GPIOError(self, "export", "Failed to export GPIO pin: " + self.pinStr)
      self.exported = True
   #Unexports the pin
   def unexport(self):
      uef = "/sys/class/gpio/unexport"
      if(not isfile(uef)):
         raise GPIOError(self, "unexport", uef + " does not exist, Cannot unexport GPIO!")
      f = open(uef, "w")
      f.write(self.pinID)
      f.close()
      if(isdir(self.pinStr)):
         raise GPIOError(self, "unexport", "Failed to unexport GPIO pin: " + self.pinStr)
      self.exported = False
   
   #Sets the mode of the GPIO pin
   def setMode(self, isOutput): 
      self.mode = "in"
      if(self.isOutput):
         self.mode = "out"
      if(not self.exported):
         export();
      pinf = self.pinStr + "/direction"
      if(not isfile(pinf):
         raise GPIOError(self, "setMode", "Unable to set " + pinf + " to " + self.mode)
      f = open(pinf, "w")
      f.write(self.mode)
      f.close()
   
   #Write a value to the specified GPIO pin
   def write(self, val):
      w = "0"
      if(val):
         w = "1"
      if(not self.exported):
         raise GPIOError(self, "write", "Pin not exported, export with setMode(mode) or export()")
      if(not self.isOutput):
         raise GPIOError(self, "write", "Cannot write to input pin, set mode with setMode(mode)!")
      #TODO: Add write code (set /sys/class/gpio/gpioXXX/value)
   #Read the value of a specified GPIO pin
   def read(self):
      #TODO: Add read code
      pass