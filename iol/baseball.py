import time
from errors import StatusError
from cli import colors

class BaseballSwitch:
	#Initialize the BaseballSwitch logic
	def __init__(self, name, settingA, settingB, positionA, positionB):
		from iol.pygpio import GPIOPin
		self.setA = GPIOPin(settingA)
		self.setB = GPIOPin(settingB)
		self.posA = GPIOPin(positionA)
		self.posB = GPIOPin(positionB)
		self.name = str(name)
		self.ignoreStatus = False #Set to true if you want to ignore the status pins (aka. dont)
		self.switchDelay = 0.5 #Switching delay
	def initGPIO(self): #Sets the states of the GPIO pins
		self.posA.setOutput()
		self.posB.setOutput()
		self.reset()
		self.setA.setInput()
		self.setB.setInput()
	def getPosition(self): #Returns an "a" or "b" depending on the position
		a = self.setA.digitalRead()
		b = self.setB.digitalRead()
		#Check the expected positions
		if(a and (not b)):
			return "a"
		if(b and (not a)):
			return "b"
		if(self.ignoreStatus):
			return "ignoring"
		#Check the unexpected positions
		if(not (a and b)):
			print(colors.red + "Error: Baseball switch is not in position A nor position B" + colors.reset)
			raise StatusError("Baseball switch", "Baseball switch (" + self.name + ") is not in position A nor position B?")
		print(colors.red + "Error: Baseball switch is in position A and position B?" + colors.reset)
		raise IOError("Baseball switch is in position A and position B?")
	def setPosition(self, isAPosition): #Sets the positions based on the isAPosition parameter, can be a string ("a" or "b") or boolean
		self.reset()
		if(type(isAPosition) == type("str")): #If they supply an "a" or "b" then decide whether or not it is "a", if so then isAPosition should be set to true
			if(isAPosition == "a"):
				isAPosition = True
			else:
				isAPosition = False
		if(isAPosition):
			self.posA.write(True)
			time.sleep(self.switchDelay)
			pos = self.getPosition()
			if(pos != "a" and (not self.ignoreStatus)):
				self.reset()
				print(colors.red + "Error: Baseball switch " + self.name + " did not switch to position A within 0.25s it is still in position " + pos + colors.reset)
				raise StatusError("Baseball switch", "Baseball switch " + self.name + " did not switch to position A within 0.25s it is still in position " + pos)
		else:
			self.posB.write(True)
			time.sleep(self.switchDelay)
			pos = self.getPosition()
			if(pos != "b" and (not self.ignoreStatus)):
				self.reset()
				print(colors.red + "Error: Baseball switch " + self.name + " did not switch to position B within 0.25s it is still in position " + pos + colors.reset)
				raise StatusError("Baseball switch", "Baseball switch " + self.name + " did not switch to position B within 0.25s it is still in position " + pos)
	def reset(self): #Resets both setting pins to False
		self.posA.write(False)
		self.posB.write(False)
	def setSwitchingDelay(self, time): #Sets the switching delay
		if(time < 0.25):
			time = 0.25
		self.switchDelay = time
	def getDelay(self): #Gets the delay in between switching
		return self.switchDelay
	def swapPos(self): #Swaps the position of the switch
		pos = self.getPosition()
		if(pos == "a"):
			self.setPosition("b")
		else:
			self.setPosition("a")

#Emulated baseball switch for testing purposes
class EmulatedBaseballSwitch:
	#Initialize the BaseballSwitch logic
	def __init__(self, name, settingA, settingB, positionA, positionB):
		from iol.pygpio import EmulatedGPIOPin
		self.setA = EmulatedGPIOPin(settingA)
		self.setB = EmulatedGPIOPin(settingB)
		self.posA = EmulatedGPIOPin(positionA)
		self.posB = EmulatedGPIOPin(positionB)
		self.name = str(name)
		self.pos = "a"
		self.switchDelay = 0.5 #Switching delay
		print(colors.yellow + "Initialized baseball switch " + str(self.name) + colors.reset)
	def initGPIO(self): #Sets the states of the GPIO pins
		self.posA.setOutput()
		self.posB.setOutput()
		self.reset()
		self.setA.setInput()
		self.setB.setInput()
		print(colors.yellow + "Initialized GPIO of baseball switch " + str(self.name) + colors.reset)
	def getPosition(self): #Returns an "a" or "b" depending on the position
		return self.pos
	def setPosition(self, isAPosition): #Sets the positions based on the isAPosition parameter, can be a string ("a" or "b") or boolean
		self.reset()
		if(type(isAPosition) == type("str")): #If they supply an "a" or "b" then decide whether or not it is "a", if so then isAPosition should be set to true
			if(isAPosition == "a"):
				isAPosition = True
			else:
				isAPosition = False
		if(isAPosition):
			print(colors.yellow + "Setting position of baseball switch " + str(self.name) + " to position A" + colors.reset)
			self.posA.write(True)
			self.pos = "a"
			time.sleep(self.switchDelay)
			pos = self.getPosition()
		else:
			print(colors.yellow + "Setting position of baseball switch " + str(self.name) + " to position B" + colors.reset)
			self.posB.write(True)
			self.pos = "b"
			time.sleep(self.switchDelay)
			pos = self.getPosition()
	def reset(self): #Resets both setting pins to False
		print(colors.cyan + "Resetting position of baseball switch " + str(self.name) + colors.reset)
		self.posA.write(False)
		self.posB.write(False)
	def setSwitchingDelay(self, time): #Sets the switching delay
		print(colors.yellow + "Setting switch delay of baseball switch " + str(self.name) + " to " + str(time) + colors.reset)
		if(time < 0.25):
			time = 0.25
		self.switchDelay = time
	def getDelay(self): #Gets the delay in between switching
		return self.switchDelay
	def swapPos(self): #Swaps the position of the switch
		print(colors.yellow + "Swapping position of baseball switch " + str(self.name) + colors.reset)
		pos = self.getPosition()
		if(pos == "a"):
			self.setPosition("b")
		else:
			self.setPosition("a")
