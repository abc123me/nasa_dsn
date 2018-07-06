import os, socket, json, sys
from cli import colors
from net import auth
from threading import Thread

#Class for deciding what to do when a client connects
class ClientHandler:
	#When the client's socket is accepted
	def onAccept(self, client):
		pass
	#Before the client has authenticated
	def preAuthenticate(self, client):
		pass
	#After the client has authenticated
	def postAuthenticate(self, client, success):
		pass
	#When the client is finished, defaults to telling the client bye!
	def onFinish(self, client):
		client.bye()
#Server object used for creating a server, the constructor takse the server port, hostname, and a credential manager
#Optional arguments below:
#checkRoot - If the server is bound to a port below port 100 it will verify that the process is root
#verbose - Prints everything to console (in cool colors!)
#queueLength - The length of the server's queue
class Server:
	def __init__(self, port, hostname, credentialManager, checkRoot=True, verbose=False, queueLength=10):
		def vprint(msg):
			if(verbose):
				print(msg)
		vprint(colors.cyan + "Server initializing..." + colors.reset)
		if(type(port) != type(65535)):
			raise TypeError("Port must be of type int")
		if(port <= 0 or port > 65535):
			raise ValueError("Port must be between 0 and 65535")
		if(checkRoot and (port >= 0 or port < 100) and os.geteuid() != 0):
			raise OSError("You need root privledges for ports between 0 and 100, disable this check by passing checkRoot=False")
		if(hostname == None):
			hostname = socket.gethostname()
		self.hostname = hostname
		self.port = port
		self.verbose = verbose
		self.queueLength = queueLength
		self.vprint = vprint
		self.serverThread = None
		self.__started = False
		self.credentialManager = credentialManager
		vprint(colors.cyan + "Server sucessfully initialized (" + str(hostname) + ":" + str(port) + ")!" + colors.reset)
	#This method starts the server, setting "allowGuestsS" to true allows guests to connect and setting "clientHanderS" 
	#will allow you to use a custom client handler
	def start(self, allowGuestsS=False, clientHanderS=ClientHandler()):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket = s
		self.vprint(colors.cyan + "ServerSocket creation was sucessful, binding it now! (" + str(self.hostname) + ":" + str(self.port) + ")!" + colors.reset)
		s.bind((self.hostname, self.port))
		self.vprint(colors.cyan + "ServerSocket binding was sucessful" + colors.reset)
		s.listen(self.queueLength)
		self.vprint(colors.yellow + "Now listening on server!" + colors.reset)
		self.serverThread = ServerThread(self, clientHandler=clientHanderS, allowGuests=allowGuestsS, verbose=self.verbose)
		self.serverThread.start()
		self.__started = True
	#This method stops the server
	def stop(self):
		self.serverThread.ignoreExceptions = True
		self.socket.close()
		self.__started = False
	#Return whether or not the server is running
	def isStarted():
		return self.__started
	#Broadcasts a message to every client connected
	def broadcast(self, msg):
		for client in clients:
			client.send("broadcast", msg)
#Internal class for processing client connections
class ServerThread(Thread):
	def __init__(self, serverInstance, clientHandler=None, allowGuests=False, verbose=False):
		super().__init__()
		def vprint(msg):
			if(verbose):
				print(msg)
		vprint(colors.cyan + "Created server thread" + (" (Guests allowed)" if allowGuests else "") + colors.reset)
		self.serverInstance = serverInstance
		self.clientHandler = clientHandler
		self.allowGuests = allowGuests
		self.ignoreExceptions = False
		self.verbose = verbose
		self.vprint = vprint
	def run(self):
		s = self.serverInstance.socket
		while(True):
			try:
				#Accept the client
				csock, caddr = s.accept()
				self.vprint(colors.cyan + "Server thread accepted client (" + str(caddr) + ")" + colors.reset)
				c = ClientInstance(csock, caddr)
				self.clientHandler.onAccept(client=c)
				#Authenticate the client unless allowGuests is true, if thats the case then we will let them authenticate themselves
				if(not self.allowGuests):
					self.vprint(colors.cyan + "Server thread authenticating client (" + str(caddr) + ")" + colors.reset)
					self.clientHandler.preAuthenticate(client=c)
					authOK = c.remoteAuthenticate(self.serverInstance.credentialManager)
					self.clientHandler.postAuthenticate(client=c, success=authOK)
					self.vprint(colors.cyan + "Server thread authenticated client (" + str(caddr) + ")" + colors.reset)
				#Were done
				self.clientHandler.onFinish(client=c)
				self.vprint(colors.cyan + "Server thread finished client (" + str(caddr) + ")" + colors.reset)
			except:
				if(self.ignoreExceptions):
					break
				print(colors.yellow + "Unexpected error in server thread (" + str(sys.exc_info()) + ")!" + colors.reset)
#Internal class for client-server negotiation, etc.
class ClientInstance:
	def __init__(self, socket, address):
		self.socket = socket
		self.address = address
		self.permissionLevel = auth.GUEST_PERMISSION_LEVEL
		self.ignoreExceptions = False
	def send(self, msg):
		self.socket.send(msg.encode())
	def sendMessage(self, content):
		toSend = {
			"type": "message",
			"from": "server",
			"content": content
		}
		self.send(json.dumps(toSend))
	def waitForResponse(self, time=0.1):
		try:
			self.socket.settimeout(time)
			data = self.socket.recv(4096);
			if not data:
				return None
			return data
		except socket.timeout:
			return None
	def request(self, whatFor, timeAllowed=0.1):
		toSend = {
			"type": "request",
			"from": "server",
			"for": whatFor
		}
		self.send(json.dumps(toSend))
		received = None
		try:
			received = json.loads(self.waitForResponse(timeAllowed))
			if(received["type"] == "request_ans" and received["content"] != None):
				return received["content"]
			return None
		except:
			return None
	def remoteAuthenticate(self, credentialManager, requests=4, timeAllowed=0.25):
		if(credentialManager == None):
			raise ValueError("Credential manager was not provided?")
		for i in range(1, requests):
			result = self.request(("username", "passwordHash", "passwordSalt"), timeAllowed)
			if(result == None):
				continue
			if(type(result) != type(("user", "hash", "salt"))):
				continue
			if(len(result) != 3):
				continue
	def bye(self):
		try:
			self.send("bye!")
			self.socket.close()
		except: pass