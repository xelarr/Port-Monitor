from scapy.all import *
import socket

PacketsArray = [[None for _ in range(1)] for _ in range(1)]
import socket

ProtocolLookupTable = {num:name[8:] for name,num in vars(socket).items() if name.startswith("IPPROTO")}

def CapturePackets(NumOfPackets):
    for i in range(0, NumOfPackets):
        sniff(filter='ip', prn=StorePacket, count=1)
    return PacketsArray

def StorePacket(pkt):
        PacketsArray.append([pkt[IP].src, pkt[IP].dst, ProtocolLookupTable[pkt.proto]])
        return PacketsArray
    


