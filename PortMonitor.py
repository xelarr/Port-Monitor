import socket
import psutil
import threading
import time
import ProcessFinder
from queue import Queue
import select
PortsArray = [[None for _ in range(1)] for _ in range(1)]
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
global var1
var1 = 0
def PortScanner(Port, var1):
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
            PortsArray.append([Port, "TCP"])
            var1 += 1
            print(Port, " is open and TCP")
            
    elif data != '':
        with print_lock:
            PortsArray.append([Port, "UDP"])
            var1 += 1
            print(Port, "is open and UDP")
    """else:
        with print_lock:
            print(Port, " is closed")"""
    "Port += 1"
    TCPSocket.close()
    UDPSocket.shutdown(socket.SHUT_RDWR)
    return PortsArray

def FindProcess(PortsArray):
    for i in range(len(PortsArray)):
        try:
            for proc in psutil.process_iter():
                for conns in proc.connections(kind='inet'):
                    if conns.laddr.port == PortsArray[i][0]:
                        PortsArray[i].append(proc.name())
                        PortsArray[i].append(proc.io_counters().other_bytes)
                        raise Exception()
        except Exception:
            continue
    return PortsArray



def GetPorts():

    def threader():
        while True:
            # gets an worker from the queue
            worker = q.get()

            # Run the example job with the avail worker in queue (thread)
            PortsArray = PortScanner(worker, var1)
        
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

    PortArray = FindProcess(PortsArray)
    "PortArray.sort()"
    return PortsArray
