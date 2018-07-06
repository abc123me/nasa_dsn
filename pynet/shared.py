_packetTypeAllowedCharacters = ""
_allowedPacketTypes = [ "rpc", "bcast", "msg", "err" ]
_maxPacketTypeLength = 0
for p in _allowedPacketTypes:
    if len(p) > _maxPacketTypeLength:
        _maxPacketTypeLength = len(p)
__packetErrors = {
    "001": "Packet too big",
    "100": "No packet type provided",
    "101": "No such packet type",
    "102": "Type of packet type is not a str",
    "103": "Packet type is over " + str(_maxPacketTypeLength) + " characters",
    "200": "No content",
    "300": "Internal server error!"
}

class PacketError(SyntaxError):
    def __init__(self, code):
        self.__code = code
    def getReason(self):
        return _packetErrors[self.__code]
    def getCode(self):
        return self.__code

class PacketFormatter:
    def checkType(t):
        if t == None:
            raise PacketError(100)
        if type(t) != type("str"):
            raise PacketError(102)
        if len(t) > _maxPacketTypeLength:
            raise PacketError(103)
        t = t.lower().strip()
        if t not in _allowedPacketTypes:
            raise PacketError(101)
        return t
    def checkContent(t, c):
        if c == None:
            raise PacketError(200)
        return c
    def createPacket(packetType, content, to=None, from_=None):
        packetType = PacketFormatter.checkType(packetType)
        content = PacketFormatter.checkContent(packetType, content)
        packet = ""
        packet = packet + "type: " + packetType + "\n"
        if to != None:
            packet = packet + "to: " + to + "\n"
        if from_ != None:
            packet = packet + "from: " + from_ + "\n"
        packet = packet + "content: " + content + "\n"
        return packet
    def getRPCContent(rpcOwner, rpcName, args):
        header = "owner=" + rpcOwner + ", name=" + rpcName
        arguments = ""
        amount = "arguments=0"
        if args != None:
            arguments = ""
            amount = "arguments=" + str(len(args))
            argID = 0
            for arg in args:
                arguments = arguments + "argument" + str(argID) + "=" + arg + "\n"
                argID = argID + 1
        return header + "\n" + amount + "\n" + arguments
        
