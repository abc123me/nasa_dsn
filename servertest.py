import atexit
from net.server import Server
from net.server import ClientHandler

class TestHandler(ClientHandler):
	def onAccept(self, client):
		print(colors.yellow + "Client accepted: " + client.address + colors.reset)
	def preAuthenticate(self, client):
		print(colors.yellow + "Client ready for authentication: " + client.address + colors.reset)
	def postAuthenticate(self, client):
		print(colors.yellow + "Client authenticated: " + client.address + colors.reset)
	def onFinish(self, client):
		print(colors.yellow + "Client finished: " + client.address + colors.reset)
		client.bye()

if(__name__ == "__main__"):
	import sys, net.auth
	cm = net.auth.CredentialManager()
	cm.loadCredentialsJSON("creds.json")
	cm.tryAddCredentials("bob", net.auth.generatePasswordHash("Password1"), net.auth.ROOT_PERMISSION_LEVEL)
	cm.tryAddCredentials("smith", net.auth.generatePasswordHash("Password1"), net.auth.ROOT_PERMISSION_LEVEL)
	cm.tryAddCredentials("eve", net.auth.generatePasswordHash("Password1"), net.auth.ROOT_PERMISSION_LEVEL)
	cm.saveCredentialsJSON("creds.json")
	s = Server(int(sys.argv[1]), "127.0.0.1", cm, checkRoot=False, verbose=True, queueLength=1)
	s.start()
	def onexit():
		cm.saveCredentialsJSON("creds.json")
		s.stop()
	atexit.register(onexit)
	
	