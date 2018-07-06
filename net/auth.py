from datetime import datetime
import binascii, os, hashlib, json
'''
PLEASE READ THE FOLLOWING BEFORE MODIFYING THE CODE:
The technique used here is known as Hashing and Salting this is a common technique used to securely manage passwords, using this
technique allows us to avoid sending the password over plain text, this prevents people who are watching the network traffic from
seeing the password. Not only does it prevent ezedropping but it also prevents people from seeing the passwords in plain text, this will hide
the passwords from mischievious employees or an accidental leak. How does it work? Hashing gives a unique signature of the text provided, the
signature cannot be reversed, allowing us to avoid storing it as plain text, the salting is not as important but prevents people from decoding
the password based on a list of common passwords and their associated hashes, which can be found via a google search

If you don't fully understand this code and the technique used,for fucks sake don't modify it since 
that easily has the potential to compromise the security of every single user relieing upon it.
'''
ROOT_PERMISSION_LEVEL = 0
ADMIN_PERMISSION_LEVEL = 1
DEFAULT_PERMISSION_LEVEL = 2
GUEST_PERMISSION_LEVEL = 3
#UTILITY CODE
def charInRange(c, mi, ma):
	return (ord(c) >= ord(mi) and ord(c) <= ord(ma))
def verifyUsername(username):
	if(username == None or username == "" or len(username) <= 0):
		return (False, "Username not provided!")
	if(type(username) != type("str")):
		return (False, "Username must be a string!")
	if(len(username) > 256):
		return (False, "Username cannot be over 256 characters!")
	for c in username:
		if((not charInRange(c, 'a', 'z')) and (not charInRange(c, 'A', 'Z')) and (not charInRange(c, '0', '9')) and (c not in "_-!@#$%^&*")): 
			return (False, "Username is not alphanumeric!")
	return (True, "Username exists!")
def generatePasswordHash(password): #Vulnerable to custom ASIC attacks, will change to scrypt later
	salt = binascii.hexlify(os.urandom(64)) #os.urandom() is used here instead since it is suitable for cryptographic usage
	hash = binascii.hexlify(hashlib.pbkdf2_hmac('sha256', password.encode("utf-8"), salt, 300000))
	return (str(hash), str(salt))
#SERVERSIDE CODE, THIS CODE IS MAINLY FOR THE SERVER --- NOT THE CLIENT
class CredentialManager:
	__credentials = {}
	
	def saveCredentialsJSON(self, loc):
		f = open(loc, "w")
		f.write(json.dumps(self.__credentials, sort_keys = False, indent = 2))
		f.close()
	def loadCredentialsJSON(self, loc):
		f = open(loc, "r")
		self.__credentials = json.loads(f.read())
		f.close()
		
	def userExists(self, username):
		if(not verifyUsername(username)[0]):
			return False
		return username in self.__credentials
	
	def removeCredentials(self, username):
		del self.__credentials[username]
	def tryAddCredentials(self, username, passwordTuple, permissionLevel):
		if(not verifyUsername(username)[0]):
			return False
		if(self.userExists(username)):
			return False
		if(type(passwordTuple) != type(("hash", "salt"))):
			raise TypeError("The passwordTuple must be a tuple containg the hash and salt of the correct password in this order: (\"hash\", \"salt\")")
			return False
		if(passwordTuple[0] == None or passwordTuple[1] == None or permissionLevel == None):
			raise ValueError("One of the supplied values are None")
			return False
		self.__credentials[username] = {
			"salt": passwordTuple[1],
			"hash": passwordTuple[0],
			"perm": permissionLevel
		}
		return True
	
	def getUsers(self):
		return self.__credentials.keys()
	def getHash(self, username):
		if(not self.userExists(username)):
			return False
		return self.__credentials[username]["hash"]
	def getSalt(self, username):
		if(not self.userExists(username)):
			return False
		return self.__credentials[username]["salt"]
	def getUserPermissionLevel():
		if(not self.userExists(username)):
			return False
		return self.__credentials[username]["perm"]