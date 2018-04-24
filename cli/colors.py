#ANSI Foreground colors
black = u"\u001b[30m"
red = u"\u001b[31m"
green = u"\u001b[32m"
yellow = u"\u001b[33m"
blue = u"\u001b[34m"
magneta = u"\u001b[35m"
magenta = magneta
cyan = u"\u001b[36m"
white = u"\u001b[37m"
#ANSI Background colors
blackB = u"\u001b[40m"
redB = u"\u001b[41m"
greenB = u"\u001b[42m"
yellowB = u"\u001b[43m"
blueB = u"\u001b[44m"
magnetaB = u"\u001b[45m"
magentaB = magnetaB
cyanB = u"\u001b[46m"
whiteB = u"\u001b[47m"
#ANSI reset "color"
reset = u"\u001b[0m"
#Unused utility function
def printColored(colorA, msg):
	print(colorA + msg + reset)
def ansi(num, end = "m"):
	return u"\u001b[" + str(num) + str(end)
if(__name__ == "__main__"):
	for j in range(30, 38):
		print(ansi(j) + str(j) + reset)