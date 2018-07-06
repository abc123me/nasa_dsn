from shared import Client
from shared import PacketFormatter
import socket, sys

class ServerHandler:
    def OnClientConnect(self, server, client):
        pass #Called when a client connects to the server
    def OnClientDisconnect(self, server, client, reason):
        pass #Called when a client is disconnected from the server
    def OnReceiveRaw(self, server, client, data):
        pass #Whenever any raw data is received
    def OnClientMessage(self, server, client, message, to):
        pass #Called when a client sends a messgae to another client or the server
    def OnClientBroadcast(self, server, client, messgae):
        pass #Called when a client attempts to broadcast titself
    def OnClientRPC(self, server, client, methodOwner, methodName, methodArguments):
        pass #Called when a client tries to invoke an RPC on the server or another client

class ClientInstance:
    def __init__(self, socket, address, uuid):
        self._sock = socket
        self._addr = address
        self._id = uuid
    def sendError(self, errorID):
        p = PacketFormatter.createPacket("err", str(errorID), from_="server")
        self._sock.sendall(p.encode())
    def sendMessage(self, msg, sender="server):
        p = PacketFormatter.createPacket("msg", str(msg), from_=sender)
        self._sock.sendall(p.encode())
    def sendBroadcast(self, msg, transmitter="server"):
        p = PacketFormatter.createPacket("bcast", str(msg), from_=transmitter)
        self._sock.sendall(p.encode())
    def callRPC(self, msg):
        
class Server:
    def __init__(self, port, host="localhost", maxClients=15, serverHandleer=ServerHandler()):
        self._addr = (port, host)
        self._serverHandler = serverHandler
        self._maxClientsConnected = maxClients
        self._clientThreads = [None * self._maxClientsConnected]
        self._isRunning = False
        
    def setAddress(self, port, host="localhost"):
        self._addr = (port, host)
    def setPort(self, port):
        self._addr[0] = port
    def setHost(self, host):
        self._addr[1] = host
    def setServerHandler(self, serverHandler):
        self._serverHandler = serverHandler
    def setMaxClients(self, clients):
        if not self.isRunning():
            self._maxClientsConnected = clients
            self._clientThreads = [None * self._maxClientsConnected]
        else:
            raise RuntimeError("Setting client amount while server is running has not yet been implemented")
        
    def _listenToClient(self, clientInstance):
        self._serverHandler.OnClientConnect(self, ci)
        try:

        except:
            self._serverHandler.OnClientDisconnect(self, ci, "Internal server error")
            print("Internal server error!")
            print(sys.exc_info[0])
        self._serverHandler.OnClientDisconnect(self, ci, "Disconnect")
    def _assignThread(self):
        for i in range(0, self._maxClientsConnected):
            thr = self._clientThreads[i]
            if thr == None:
                return i
            if not thr.isalive():
                return i
        return -1
    def _listen(self):
        self._sock.listen(self._queue)
        self._clients = {}
        while True:
            if self._stopServer: break
            cli, adr = self._sock.accept()
            ci = ClientInstance(cli, adr, clientID)
            clientID = clientID + 1
            threadID = self._assignThread()
            if threadID >= 0:
                self._clientThreads[i] = threading.Thread(target=self._listenToClient, name="ClientListenerThread", args=(ci))
            self._clients.add(ci)
            
    def startServer(self, queue=3):
        self._stopServer = False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(self._addr)
        self._queue = queue
        self._sock = s
        self._serverThread = threading.Thread(target=self._listen, name="ServerThread")
        self._clientThreads = [None * self._maxClientsConnected]
        self._isRunning = True
    def stopServer(self):
        self._sock.close()
        self._sock = None
        self._serverThread = None
        self._stopServer = True
        self._clientThreads = [None * self._maxClientsConnected]
        self._isRunning = False
    def getConnectedClients(self):
        return self._clients
    def isRunning(self):
        return self._isRunning
