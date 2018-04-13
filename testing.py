def decibelsToBinary(num):
	val = [False] * 8
	for i in range(7, -1, -1):
		mdbv = 2 ** (i - 2)
		if(num >= mdbv):
			num = num - mdbv;
			val[i] = True
			print("num " + str(num) + " > " + str(mdbv))
	return val
print(decibelsToBinary(10.25))