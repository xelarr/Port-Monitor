import psutil

def GetBytesSent(self, Array):
        
     
        
        Activity = psutil.net_io_counters()
        PreviousTotal = Activity[0]
        time.sleep(0.5)
        Activity = psutil.net_io_counters()
        NewTotal = Activity[0]
        NewValue = (NewTotal - PreviousTotal)
        Array.append(NewValue)
        if len(Array) > 10:
                Array.pop(0)
        return Array


def GetBytesRecv(self, Array):
        
     
        
        Activity = psutil.net_io_counters()
        PreviousTotal = Activity[1]
        time.sleep(0.5)
        Activity = psutil.net_io_counters()
        NewTotal = Activity[1]
        NewValue = (NewTotal - PreviousTotal)
        Array.append(NewValue)
        if len(Array) > 10:
                Array.pop(0)
        return Array
