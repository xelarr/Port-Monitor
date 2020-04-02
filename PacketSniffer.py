from scapy.all import *
import socket


ProtocolLookupTable = {num:name[8:] for name,num in vars(socket).items() if name.startswith("IPPROTO")}

def CapturePackets(NumOfPackets):
    PacketsArray = [[None for _ in range(1)] for _ in range(1)]
    def GetPackets(NumOfPackets):
        for i in range(0, NumOfPackets):
            sniff(filter='ip', prn=StorePacket, count=1)
        return PacketsArray

    def StorePacket(pkt):
        try:
            if (1 < pkt[IP].ttl <= 30) or (64 < pkt[IP].ttl <= 98) or (128 < pkt[IP].ttl <= 225):
                PacketsArray.append([pkt[IP].src, pkt[IP].dst, ProtocolLookupTable[pkt.proto],  pkt[IP].ttl])
            else:
                PacketsArray.append([pkt[IP].src, pkt[IP].dst, ProtocolLookupTable[pkt.proto], "Length: {} | Flags: {} | ID: {} | TTL: {}".format(pkt[IP].len, pkt[IP].flags, pkt[IP].id, pkt[IP].ttl)])
        except KeyError:
            PacketsArray.append([pkt[IP].src, pkt[IP].dst, "IGMP"])
        return PacketsArray
    PacketsArray = GetPackets(NumOfPackets)
    PacketsArray.pop(0)
    return PacketsArray
    


