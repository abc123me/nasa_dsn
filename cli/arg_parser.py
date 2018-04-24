from cli import colors

def __makeAlphanumeric(arg): #Makes a string alphanumeric
	out = ""
	for i in range(0, len(arg)):
		c = arg[i]
		v = ord(c)
		if((v >= ord('a') and v <= ord('z')) or (v >= ord('A') and v <= ord('Z')) or (v >= ord('0') and v <= ord('9'))): #Check if it is alphanumeric
			out = out + c
			continue
	return out
def __getHead(arg): #Determines whether or not the argument should have a -- or - on it
	if(len(arg) > 1):
		return "--"
	return "-"
def __forceArr(data): #Checks for an array (also forces a string to be a 1-item array)
	if(data == None)
		return None
	if(type(data) == type("str"))
		return [ data ]
	if(type(data) == type(["arr"]))
		return data
	raise TypeError("Invalid type, you must use a string or list")
def __cleanArr(arr): #Cleans all strings in an array and only allows fully alphanumeric strings, if there are no alphanumeric strings it will return None
	out = []
	for obj in arr:
		if(obj == None):
			continue
		if(type(obj) != type("str")):
			obj = str(obj)
		obj = __makeAlphanumeric(obj)
		if(len(obj) <= 0):
			continue
		out.append(obj)
	if(len(out) == 0):
		return None
	return out

class Argument:
	def __init__(self, name, aliases, params, desc, action):
		self.name = name
		self.aliases = __cleanArr(__forceArr(aliases))
		self.action = action
		self.params = __cleanArr(__forceArr(params))
		self.desc = desc
	def __str__(self):
		nameStr = __getHead(self.name) + self.name
		if(self.aliases != None):
			for alias in self.aliases:
				nameStr = nameStr + ", " + __getHead(alias) + alias
		paramStr = ""
		if(self.params != None):
			for param in self.params:
				paramStr = paramStr + " [" + param + "]"
		return nameStr + paramStr + ": " + self.desc
  
def parseArgs(validArgs, userArgs):
	for i in range(0, len(userArgs)):
		arg = userArgs[i]
    
    