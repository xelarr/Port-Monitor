from tkinter import *
from tkintertable import *
import PacketSniffer
import PortMonitor
import HomeGraph
import PortGraph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
from random import randint
import psutil

class CreateToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.close)
    def enter(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(self.tw, text=self.text, justify='left', background='yellow', relief='solid', borderwidth=1, font=("times", "8", "normal"))
        label.pack(ipadx=1)
    def close(self, event=None):
        if self.tw:
            self.tw.destroy()


class Page(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
    def show(self):
        self.lift()

class Home(Page):
    def __init__(self, master=None):
        Page.__init__(self, master)
        AlertsPage = Alerts(self)
        PortPage = Port(self)
        Home.BytesSent = []
        Home.BytesRecv = []
        Home.GraphCanvas = Canvas(self)
        Home.Rectangle = Home.GraphCanvas.create_rectangle(650, 580, 1150, 740, fill="white")
        Home.GraphCanvas.pack(fill=BOTH, expand=1)
        Home.ContinuePlotting = False
        Fig = Figure()

        

        
        Home.Ax = Fig.add_subplot(111)
        Home.Ax.get_xaxis().set_visible(False)
        Home.Ax.grid()
 
        Home.Graph = FigureCanvasTkAgg(Fig, master=Home.GraphCanvas)
        Home.Graph.get_tk_widget().place(x=710, y=590, height= 150, width=430)
        self.PortTable = Treeview(self, selectmode='browse')
        self.PortTable.pack()
        self.PortTable.place(x = 0, y = 20, height = 500, width = 1190)

        ScrollBarY = Scrollbar(self, orient='vertical')
        ScrollBarY.config(command=self.PortTable.yview)
        ScrollBarY.pack(side=RIGHT, fill=Y)
        
        self.PortTable['columns'] = ('Port No.', 'Protocol', 'PID', 'Application', 'Address')
        self.PortTable['show'] = 'headings'
        self.PortTable.heading("Port No.", text='Port No.')
        self.PortTable.column("Port No.", anchor="center", width=30)
        self.PortTable.heading('Protocol', text='Protocol')
        self.PortTable.column('Protocol', anchor='center', width=100)
        self.PortTable.heading('PID', text='PID')
        self.PortTable.column('PID', anchor='center', width=30)
        self.PortTable.heading('Application', text='Application')
        self.PortTable.column('Application', anchor='center', width=100)
        self.PortTable.heading('Address', text='Address')
        self.PortTable.column('Address', anchor='center', width=100)

        
        Label(self, text='Number of Alerts: ', borderwidth=1).place(x=50, y=600)
        Label(self, text='Highest Priority: ', borderwidth=1).place(x=50, y=650)
        b = Button(self, text='Go To Alerts', command=master.LiftAlerts)
        b.place(x=150, y=700)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        Home.PortsArray = Button(self, command=self.UpdatePorts, text="Update Table").place(x= 540,y=700)
        Home.PortsArray = PortMonitor.GetPorts()
            
        
        Index = Iid = 0
        
        for row in Home.PortsArray:
            self.PortTable.insert("", Index, Iid, values=row)
            Index = Iid = Index + 1

        Home.PortAnswerBox = Entry(self)
        Home.PortAnswerBox.place(x=520, y=550)
        Button(self, command=lambda:[master.LiftPort(), Port.RecievePort(Port)], text="View Port").place(x=620, y=548)
        
        Button(self, text="Start/Stop", command=Home.ChangeState).place(x=800, y=548)
        Label(self, text="Bytes", borderwidth=1, background='white').place(x=660, y=650)
    
    def ChangeToFalse():
        Home.ContinuePlotting = False
        Home.GraphUpdater()
        
    def ChangeState():
        print("updated")
        if Home.ContinuePlotting == True:
            Home.ContinuePlotting = False
        else:
            Home.ContinuePlotting = True
        Home.GraphUpdater()

    def GraphUpdater():
        if Home.ContinuePlotting == True:
            Home.Ax.cla()
            Home.Ax.grid()
            BytesSent = HomeGraph.GetBytesSent(Home,Home.BytesSent)
            BytesRecv = HomeGraph.GetBytesRecv(Home,Home.BytesRecv)
            BytesSentLine = Home.Ax.plot(range(len(Home.BytesSent)), BytesSent, marker='o', color='orange', label='Bytes Sent')
            BytesRecvLine = Home.Ax.plot(range(len(Home.BytesRecv)), BytesRecv, marker='o', color='blue', label = 'Bytes Recieved')
            Home.Ax.legend(loc='upper left', fontsize=8)
            Home.Graph.draw()
            root.update_idletasks()
            root.after(200, Home.GraphUpdater)
    
    def UpdatePorts(self):
        PortsArray = PortMonitor.GetPorts()
        self.UpdateTable(PortsArray)
        return PortsArray
    def UpdateTable(self, PortsArray):
        for i in self.PortTable.get_children():
            self.PortTable.delete(i)
        Index = Iid = 0
        for row in PortsArray:
            self.PortTable.insert("",Index, Iid, values=row)
            Index = Iid = Index + 1
    def GetSelectedPort(self):
        PortNumberString = Home.PortAnswerBox.get()
        PortNumberInt = int(PortNumberString)
        return PortNumberInt
        
class Port(Page):
    def __init__(self, master=None):
        Page.__init__(self, master)
        Port.Canvas = Canvas(self)
        Port.OpenCloseRectangle = Port.Canvas.create_rectangle(800, 200, 1000, 300, fill="IndianRed1")
        Port.GraphRectangle = Port.Canvas.create_rectangle(50, 175, 770, 750, fill="white")
        Port.Canvas.pack(fill=BOTH, expand=1)
        Port.ContinuePlotting = False
        Fig = Figure()
        Port.Bytes=[]
        Port.Ax = Fig.add_subplot(111)
        Port.Ax.get_xaxis().set_visible(False)
        Port.Ax.grid()
        Port.PortNumber = 0
        Port.Graph = FigureCanvasTkAgg(Fig, master=Port.Canvas)
        Port.Graph.get_tk_widget().place(x=60, y=190, height=550, width=700)
        LabelFrame(self, text="Process").place(x=800,y=320, height=50,width=200)
        LabelFrame(self, text="Protocol").place(x=800,y=380, height=50,width=200)
        LabelFrame(self, text="Address").place(x=800,y=440, height=50,width=200)
        self.PortLabelFrame = LabelFrame(self, text="Port Number").place(x=50,y=50,height=75,width=200)
        Port.PortLabel = Label(self, text="N/A")
        Port.PortLabel.place(x=60,y=80)
        Port.ProcessLabel = Label(self, text="N/A")
        Port.ProcessLabel.place(x=820,y=340)
        Port.ProtocolLabel = Label(self, text="N/A")
        Port.ProtocolLabel.place(x=820,y=400)
        Port.AddressLabel = Label(self, text="N/A")
        Port.AddressLabel.place(x=820,y=460)
        Port.OpenorClosed = Label(self, text="Closed", background="IndianRed1")
        Port.OpenorClosed.place(x=875, y=235)

        Button(self, text="Start/Stop", command=Port.ChangeState).place(x=800, y=100)
    def RecievePort(self):
        Port.PortNumber = Home.GetSelectedPort(self)
        ArrayLength = len(Home.PortsArray)
        Found = False
        for i in range (ArrayLength):
            if (Home.PortsArray[i][0] == Port.PortNumber):
                PortProtocol = Home.PortsArray[i][1]
                PortProcess = Home.PortsArray[i][2]
                PortAddress = Home.PortsArray[i][3]
                Port.Canvas.itemconfig(Port.OpenCloseRectangle, fill="chartreuse2")
                Port.OpenorClosed['text'] = "Open"
                Port.OpenorClosed['background'] = "chartreuse2"
                Found = True
        if Found == False:
            PortProtocol = "N/A"
            PortProcess = "N/A"
            PortAddress = "N/A"
            Port.Canvas.itemconfig(Port.OpenCloseRectangle, fill="IndianRed1")
            Port.OpenorClosed['text'] = "Closed"
            Port.OpenorClosed['background'] = "IndianRed1"
                
        Port.PortLabel['text'] = Port.PortNumber
        Port.ProtocolLabel['text'] = PortProtocol
        Port.ProcessLabel['text'] = PortProcess
        Port.AddressLabel['text'] = PortAddress
    

    def ChangeToFalse():
        Port.ContinuePlotting = False
        Port.GraphUpdater()
        
    def ChangeState():
        print("updated")
        if Port.ContinuePlotting == True:
            Port.ContinuePlotting = False
        else:
            Port.ContinuePlotting = True
        Port.GraphUpdater()

    def GraphUpdater():
        if Port.ContinuePlotting == True:
            Port.Ax.cla()
            Port.Ax.grid()
            Bytes = PortGraph.GetBytes(Port, Port.PortNumber, Port.Bytes)
            print("updated")
            BytesLine = Port.Ax.plot(range(len(Port.Bytes)), Port.Bytes, marker='o', color='blue', label = 'Bytes')
            Port.Ax.legend(loc='upper left', fontsize=8)
            Port.Graph.draw()
            root.update_idletasks()
            root.after(200, Port.GraphUpdater)

        
class Capture(Page):
    
    def __init__(self, master=None):
        Page.__init__(self, master)
        self.CaptureTable = Treeview(self)
        self.CaptureTable.pack()
        self.CaptureTable.place(x = 0, y = 0, height = 650, width = 1170)
        SourceLabel = Label(self, text='i', background= 'white')
        SourceLabel.place(y=5, x= 280)
        CreateToolTip(SourceLabel, 'The source of the packet')

        DestinationLabel = Label(self, text='i', background= 'white')
        DestinationLabel.place(y=5, x= 565)
        CreateToolTip(DestinationLabel, 'The destination of the packet')

        ProtocolLabel = Label(self, text='i', background= 'white')
        ProtocolLabel.place(y=5, x= 855)
        CreateToolTip(ProtocolLabel, 'The protocol of the packet')

        InfoLabel = Label(self, text='i', background= 'white')
        InfoLabel.place(y=5, x= 1130)
        CreateToolTip(InfoLabel, 'The length, fragmentation settings, id and ttl of the packet')
        
        
        ScrollBarY = Scrollbar(self, orient='vertical')
        ScrollBarY.config(command=self.CaptureTable.yview)
        ScrollBarY.pack(side=RIGHT, fill=Y)
        self.CaptureTable['columns'] = ['Source', 'Destination', 'Protocol', 'Information']
        self.CaptureTable['show'] = 'headings'
        self.CaptureTable.heading('Source', text='Source')
        self.CaptureTable.column('Source', anchor="w", width=100)
        self.CaptureTable.heading('Destination', text='Destination')
        self.CaptureTable.column('Destination', anchor='center', width=100)
        self.CaptureTable.heading('Protocol', text='Protocol')
        self.CaptureTable.column('Protocol', anchor='center', width=100)
        self.CaptureTable.heading('Information', text='Information')
        self.CaptureTable.column('Information', anchor='center', width=100)
        self.treeview = self.CaptureTable
        Capture.AnswerBox = Entry(self)
        Capture.AnswerBox.place(x=550, y=700)
        CaptureArray = Button(self, command=self.CapturePackets, text="Capture Packets").place(x=700, y=698)
        Label(self, text='Enter the number of packets to sniff', borderwidth=1).place(x=540, y=670)

        
        
    def CapturePackets(self):
        messagebox.showinfo('Port Monitor', 'Capturing Packets')
        PacketsNumberString = self.AnswerBox.get()
        PacketsNumberInt = int(PacketsNumberString)
        CaptureArray = PacketSniffer.CapturePackets(PacketsNumberInt)
        self.UpdateTable(CaptureArray)
    def UpdateTable(self, CaptureArray):
        for i in self.CaptureTable.get_children():
            self.CaptureTable.delete(i)
        Index = Iid = 0
        for row in CaptureArray:
            self.CaptureTable.insert("",Index, Iid, values=row)
            Index = Iid = Index + 1
        
class Alerts(Page):
    def __init__(self, master=None):
        Page.__init__(self, master)
        AlertTable = Treeview(self)
        AlertTable.pack()
        AlertTable.place(x = 0, y = 0, height = 700, width = 1170)

        ScrollBarY = Scrollbar(self, orient='vertical')
        ScrollBarY.config(command=AlertTable.yview)
        ScrollBarY.pack(side=RIGHT, fill=Y)
        
        AlertTable['columns'] = ('Status', 'Info', 'Priority', 'Solved')
        AlertTable.heading("#0", text='Port', anchor='w')
        AlertTable.column("#0", anchor="w", width=100)
        AlertTable.heading('Status', text='Status')
        AlertTable.column('Status', anchor='center', width=100)
        AlertTable.heading('Info', text='Info')
        AlertTable.column('Info', anchor='center', width=100)
        AlertTable.heading('Priority', text='Priority')
        AlertTable.column('Priority', anchor='center', width=100)
        AlertTable.heading('Solved', text='Solved')
        AlertTable.column('Solved', anchor='center', width=100)
        self.treeview = AlertTable

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        self.HomePage = Home(self)
        self.PortPage = Port(self)
        self.CapturePage = Capture(self)
        self.AlertsPage = Alerts(self)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)
        
        self.LiftHome()
        
        self.HomePage.place(in_=container, x=0, y=25, relwidth=1, relheight=1)
        self.PortPage.place(in_=container, x=0, y=25, relwidth=1, relheight=1)
        self.CapturePage.place(in_=container, x=0, y=25, relwidth=1, relheight=1)
        self.AlertsPage.place(in_=container, x=0, y=25, relwidth=1, relheight=1)
        HomeButton = Button(self, text="Home", command=lambda:[self.LiftHome()])
        HomeButton.place(x=0, y=0, width=400)
        CaptureButton = Button(self, text="Capture", command=lambda:[self.LiftCapture(), Home.ChangeToFalse()])
        CaptureButton.place(x=400, y=0, width = 400)
        AlertsButton = Button(self, text="Alerts", command=lambda:[self.LiftAlerts(), Home.ChangeToFalse()])
        AlertsButton.place(x=800, y=0, width = 400)
    def LiftHome(self):
        self.HomePage.lift()
    def LiftAlerts(self):
        Home.ChangeToFalse()
        self.AlertsPage.lift()
    def LiftCapture(self):
        Home.ChangeToFalse()
        self.CapturePage.lift()
    def LiftPort(self):
        Home.ChangeToFalse()
        self.PortPage.lift()
        

# initialize tkinter
root = Tk()
app = Window(root)
# set window title
root.wm_title("Port Monitor")
root.wm_geometry("1200x800")
root.resizable(width=False, height=False)
# show window
"root.after(500, Home.gui_handler())"
root.mainloop()
