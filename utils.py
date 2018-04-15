def decibelsToBinary(num): #Converts the decibel value input to the binary value output that needs to be written to the GPIO Pins
	val = [False] * 8
	for i in range(7, -1, -1):
		mdbv = 2 ** (i - 2)
		if(num >= mdbv):
			num = num - mdbv;
			val[i] = True
	return val