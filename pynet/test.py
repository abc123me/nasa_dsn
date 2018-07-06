from client import Client
from time import sleep
import atexit

class MyClientHandler:
    def OnConnect(self, c):
        print("Client connected to server!")
        c.sendMessage("Hello", "server")
        c.broadcast("This is a broadcast!")
        c.invokeRPC("server", "kick", ["client11"])
    def OnDisconnect(self, c, reason):
        print("Client disconnected from server, Reason: " + reason)
    def OnReceiveRaw(self, c, data):
        try:
            print("Client recieved " + str(len(data)) + " bytes of raw data: " + data.decode("utf-8"))
        except UnicodeDecodeError:
            print("Client recieved " + str(len(data)) + " bytes of raw data, failed to decode")
    def OnMessageReceived(self, c, sender, msg):
        print("Recieved message from client: " + str(sender) + ", " + msg) 
    def OnBroadcastReceived(self, c, msg):
        print("Recieved broadcast: " + msg)
    def OnRPCInvoke(self, c, invoker, methodName, methodArguments):
        print("Attempt to invoke RPC " + methodName + " with arguments: " + str(methodArguments))


c = Client()
c.setHandler(MyClientHandler())
c.connect("localhost", 1234, 3, 0.25)
c.startListening()
print("Waiting!")
c.waitForDisconnect()
print("Done!")
atexit.register(c.stopListening)
atexit.register(c.disconnect)

