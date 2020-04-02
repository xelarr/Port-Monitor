import socket
import psutil
import threading
import time
from queue import Queue
import select
import scapy
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
Host = get_ip()
LoopbackAddress = '127.0.0.1'
print_lock = threading.Lock()
print(Host)
Port = 0 #First port.
def PortScanner(Port, PortsArray):
    "while Port <= 65535: #Port 65535 is last port you can access."
    data = ''
    TCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPResult1 = TCPSocket.connect_ex((Host, Port))
    TCPResult2 = TCPSocket.connect_ex((LoopbackAddress, Port))
    UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        UDPSocket.bind((Host, Port))
    except:
        data = 'open'
    
    UDPSocket.shutdown(socket.SHUT_RDWR)
    UDPSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        UDPSocket.bind((LoopbackAddress, Port))
    except:
        data = 'open'
    ready = select.select([UDPSocket], [], [], 0.5)
    if ready[0]:
        data = UDPSocket.recv(1024)

    if TCPResult1 == 0 or TCPResult2 == 0:
        with print_lock:
            PortsArray.append([])
            PortsArray[((len(PortsArray)) -1)].append([])
            PortsArray[((len(PortsArray)) -1)].append([])
            PortsArray[((len(PortsArray)) -1)][0] = Port
            PortsArray[((len(PortsArray)) -1)][1] = "TCP"            
    elif data != '':
        with print_lock:
            PortsArray.append([])
            PortsArray[((len(PortsArray)) -1)].append([])
            PortsArray[((len(PortsArray)) -1)].append([])
            PortsArray[((len(PortsArray)) -1)][0] = Port
            PortsArray[((len(PortsArray)) -1)][1] = "UDP"
    """else:
        with print_lock:
            print(Port, " is closed")"""
    "Port += 1"
    TCPSocket.close()
    UDPSocket.shutdown(socket.SHUT_RDWR)
    return PortsArray

def FindProcess(PortsArray, PortProcessGot):
        
    for proc in psutil.process_iter():
        for conns in proc.connections(kind='inet'):
            try:
                for i in range(len(PortsArray)):
                    if conns.laddr.port == PortsArray[i][0]:
                        if PortProcessGot[i] == True:
                            raise Exception()
                        else:
                            PortsArray[i].append([])
                            PortsArray[i].append([])
                            PortsArray[i].append([])
                            PortsArray[i][2] = proc.pid
                            PortsArray[i][3] = proc.name()
                            PortsArray[i][4] = conns.laddr.ip
                            PortProcessGot[i] = True
            except Exception:
                continue
    return PortsArray


def GetPorts():
    PortsArray = [[0] * 3 for i in range(1)]
    PortProcessGot = [False for _ in range(65535)]
    PortArray = ThreadedPortFinder(PortsArray, PortProcessGot)
    return PortArray


def ThreadedPortFinder(PortsArray, PortProcessGot):
    def threader():
        while True:
            # gets an worker from the queue
            worker = q.get()

            # Run the example job with the avail worker in queue (thread)
            PortScanner(worker, PortsArray)
            # completed with the job
            q.task_done()

    q = Queue()
    for x in range(5000):
         t = threading.Thread(target=threader)

         # classifying as a daemon, so they will die when the main dies
         t.daemon = True

         # begins, must come after daemon definition
         t.start()

    start = time.time()

    for worker in range(1,65535):
        q.put(worker)

    q.join()
    print("Ports Found")
    PortProcessArray = FindProcess(PortsArray, PortProcessGot)
    print("Processes Found")
    PortProcessArray.pop(0)
    PortProcessArray.sort()
    return PortProcessArray


