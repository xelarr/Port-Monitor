from scapy.all import *



def GetBytes(self, PortNumber, Array):
    Total = 0
    def GetPackets(PortNumber):
        print("updated")
        sniff(filter="ip and port {}".format(PortNumber), prn=CalculateBytes, timeout=1)
        

        
    def CalculateBytes(pkt):
        print(len(pkt))
        print(pkt.sprintf("%IP.len%"))
        Total += int(len(pkt))
    
 
    GetPackets(PortNumber)
    Array.append(Total)
    if len(Array) > 10:
                Array.pop(0)
    return Array

