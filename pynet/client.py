from shared import Client
from shared import PacketFormatter
from threading import Thread
import socket, sys, time

class ClientHandler:
    def OnConnect(self, c):
        pass #Called wghen the client is connected to the server
    def OnDisconnect(self, c, reason):
        pass #Called when the client is disconnected from the server
    def OnReceiveRaw(self, c, data):
        pass #Whenever any raw data is received
    def OnMessageReceived(self, c, sender, msg):
        pass #Called when a message is received from another client or the server
    def OnBroadcastReceived(self, c, msg):
        pass #Called when a broadcast is received
    def OnRPCInvoke(self, c, invoker, methodName, methodArguments):
        pass #Called when an RPC is invoked

class Client:
    def __init__(self):
        self._handler = ClientHandler()
        self._listeningThread = Thread(target=self._listen)
        self._stopListeningThread = False
        self._recvbufsize = 4096
        self._socket = None
        
    def setHandler(self, handler):
        self._handler = handler
    def setRecieveBufferSize(self, bufsize):
        self._recvbufsize = bufsize
        
    def connect(self, serverIP, serverPort, backlog=3, timeout=0.25):
        s = socket.socket()
        s.connect((serverIP, serverPort))
        self._socket = s
        self._connected = True
        self._handler.OnConnect(self)
    def disconnect(self):
        if not self._connected: raise RuntimeError("Please connect before disconnecting!")
        if self.isListening(): raise RuntimeError("Please stop listening before disconnceting")
        if self._socket != None: self._socket.close()
        self._socket = None
        self._connected = False
        self._handler.OnDisconnect(self, "Disconnected")
    def waitForDisconnect(self, t=0.1):
        while not self.isConnected():
            time.sleep(t)
        while self.isConnected():
            time.sleep(t)
    def isConnected(self):
        return self._connected

    def _processData(self, data):
        self._handler.OnReceiveRaw(self, data)
        pass
    def _listen(self):
        while not self._stopListeningThread:
            data = self._socket.recv(self._recvbufsize)
            if not data:
                self._handler.OnDisconnect(self, "Server closed")
                self._connected = False
                self._socket = None
                break
            self._processData(data)
    def startListening(self, threaded=True):
        self._stopListeningThread = False
        self._listeningThread.start()
    def stopListening(self):
        self._stopListeningThread = True
    def isListening(self):
        self._listeningThread.is_alive()

    def sendRaw(self, data):
        self._socket.send(bytes(data))
    def sendMessage(self, msg, to):
        pkt = PacketFormatter.createPacket("msg", msg, to)
        self.sendRaw(pkt.encode())
    def broadcast(self, msg):
        pkt = PacketFormatter.createPacket("bcast", msg)
        self.sendRaw(pkt.encode())
    def invokeRPC(self, rpcOwner, rpcName, rpcArguments):
        pkt = PacketFormatter.createPacket("rpc", PacketFormatter.getRPCContent(rpcOwner, rpcName, rpcArguments))
        self.sendRaw(pkt.encode())
