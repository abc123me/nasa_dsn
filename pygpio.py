# A Semi decent GPIO lbrary for python3
import sys
if(sys.version_info[0] < 3): #Check python version
    raise "This only supports python3!"

from subprocess import call
from os.path import isfile
from os.path import isdir
class GPIO:
  pinID = 0;
  pinStr = ""
  isOutput = False
  exported = False
  
  def __init__(self, pin): #Constructor called when object is created
    self.pinID = pin
    self.exported = False
  def __del__(self): #Deconstructer called when object is no longer used
    self.unexport()
    
  #Export and unexport subroutines handled by setMode and destructor
  def export(self): #Exports the pin
    if(not isfile("/sys/class/gpio/export")):
      raise "/sys/class/gpio/export does not exist!"
    f = open("/sys/class/gpio/export", "w")
    f.write(pinID);
    f.close()
    pinStr = "/sys/class/gpio" + pinID
    if(not isdir(pinStr)):
      raise "Failed to export GPIO pin: " + pinStr
    exported = True
  def unexport(self): #Unexports the pin
    #TODO: Add GPIO unexport code
    exported = False
    
  def setMode(self, isOutput): #Sets the mode of the GPIO pin
    self.mode = "in"
    if(isOutput):
      self.mode = "out"
    if(not exported):
      export();
    #TODO: Add setmode code (set /sys/class/gpio/gpioXXX/direction)
    
  def write(self, val): #Write a value to the specified GPIO pin
    w = "0"
    if(val):
      w = "1"
    if(not exported):
      raise "Pin not exported, export with export() or setMode(mode)"
    if(not isOutput):
      raise "Cannot write to input pin, set mode with setMode(mode)!"
    #TODO: Add write code (set /sys/class/gpio/gpioXXX/value)
    
  def read(self):