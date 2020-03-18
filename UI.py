from tkinter import *
from tkintertable import *
import PacketSniffer
import PortMonitor
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

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
        Home.GraphCanvas = Canvas(self)
        Home.Rectangle = Home.GraphCanvas.create_rectangle(650, 580, 1100, 740, fill="white")
        Home.GraphCanvas.pack(fill=BOTH, expand=1)
        self.PortTable = Treeview(self, selectmode='browse')
        self.PortTable.pack()
        self.PortTable.place(x = 0, y = 20, height = 500, width = 1190)

        scrollbary = Scrollbar(self, orient='vertical')
        scrollbary.config(command=self.PortTable.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        
        self.PortTable['columns'] = ('Port No.', 'Application', 'Protocol', 'Address', 'Recieving(B/sec)', 'View')
        self.PortTable['show'] = 'headings'
        self.PortTable.heading("Port No.", text='Port No.')
        self.PortTable.column("Port No.", anchor="center", width=30)
        self.PortTable.heading('Application', text='Application')
        self.PortTable.column('Application', anchor='center', width=100)
        self.PortTable.heading('Protocol', text='Protocol')
        self.PortTable.column('Protocol', anchor='center', width=100)
        self.PortTable.heading('Address', text='Address')
        self.PortTable.column('Address', anchor='center', width=100)
        self.PortTable.heading('Recieving(B/sec)', text='Recieving(B/sec)')
        self.PortTable.column('Recieving(B/sec)', anchor='center', width=100)
        self.PortTable.heading('View', text='View')
        self.PortTable.column('View', anchor='center', width=30)
       
        
        Label(self, text='Number of Alerts: ', borderwidth=1).place(x=50, y=600)
        Label(self, text='Highest Priority: ', borderwidth=1).place(x=50, y=650)
        Button(self, text='Go To Alerts', command=master.LiftAlerts).place(x=150, y=700)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        Home.PortsArray = Button(self, command=self.UpdatePorts, text="Update Table").place(x= 540,y=700)
        
        Home.PortsArray = PortMonitor.GetPorts()
            
        index = iid = 0
        
        for row in Home.PortsArray:
            self.PortTable.insert("", index, iid, values=row)
            index = iid = index + 1

        Home.PortAnswerBox = Entry(self)
        Home.PortAnswerBox.place(x=520, y=550)
        Button(self, command=lambda:[master.LiftPort(), Port.RecievePort(Port)], text="View Port").place(x=620, y=548)
        
    def UpdatePorts(self):
        PortsArray = PortMonitor.GetPorts()
        self.UpdateTable(PortsArray)
        return PortsArray
    def UpdateTable(self, PortsArray):
        for i in self.PortTable.get_children():
            self.PortTable.delete(i)
        index = iid = 0
        for row in PortsArray:
            self.PortTable.insert("",index, iid, values=row)
            index = iid = index + 1
    def GetSelectedPort(self):
        PortNumberString = Home.PortAnswerBox.get()
        PortNumberInt = int(PortNumberString)
        return PortNumberInt
        
class Port(Page):
    def __init__(self, master=None):
        Page.__init__(self, master)
        Port.canvas = Canvas(self)
        Port.OpenCloseRectangle = Port.canvas.create_rectangle(800, 200, 1000, 300, fill="IndianRed1")
        Port.GraphRectangle = Port.canvas.create_rectangle(50, 175, 770, 750, fill="white")
        Port.canvas.pack(fill=BOTH, expand=1)
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
    
    def RecievePort(self):
        PortNumber = Home.GetSelectedPort(self)
        ArrayLength = len(Home.PortsArray)
        Found = False
        for i in range (ArrayLength):
            if (Home.PortsArray[i][0] == PortNumber):
                PortProtocol = Home.PortsArray[i][1]
                PortProcess = Home.PortsArray[i][2]
                PortAddress = Home.PortsArray[i][3]
                Port.canvas.itemconfig(Port.OpenCloseRectangle, fill="chartreuse2")
                Port.OpenorClosed['text'] = "Open"
                Port.OpenorClosed['background'] = "chartreuse2"
                Found = True
        if Found == False:
            PortProtocol = "N/A"
            PortProcess = "N/A"
            PortAddress = "N/A"
            Port.canvas.itemconfig(Port.OpenCloseRectangle, fill="IndianRed1")
            Port.OpenorClosed['text'] = "Closed"
            Port.OpenorClosed['background'] = "IndianRed1"
                
        Port.PortLabel['text'] = PortNumber
        Port.ProtocolLabel['text'] = PortProtocol
        Port.ProcessLabel['text'] = PortProcess
        Port.AddressLabel['text'] = PortAddress
    

        
class Capture(Page):
    
    def __init__(self, master=None):
        Page.__init__(self, master)
        self.CaptureTable = Treeview(self)
        self.CaptureTable.pack()
        self.CaptureTable.place(x = 0, y = 0, height = 650, width = 1170)

        scrollbary = Scrollbar(self, orient='vertical')
        scrollbary.config(command=self.CaptureTable.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
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
        PacketsNumberString = self.AnswerBox.get()
        PacketsNumberInt = int(PacketsNumberString)
        CaptureArray = PacketSniffer.CapturePackets(PacketsNumberInt)
        self.UpdateTable(CaptureArray)
    def UpdateTable(self, CaptureArray):
        for i in self.CaptureTable.get_children():
            self.CaptureTable.delete(i)
        index = iid = 0
        for row in CaptureArray:
            self.CaptureTable.insert("",index, iid, values=row)
            index = iid = index + 1
        
class Alerts(Page):
    def __init__(self, master=None):
        Page.__init__(self, master)
        AlertTable = Treeview(self)
        AlertTable.pack()
        AlertTable.place(x = 0, y = 0, height = 700, width = 1170)

        scrollbary = Scrollbar(self, orient='vertical')
        scrollbary.config(command=AlertTable.yview)
        scrollbary.pack(side=RIGHT, fill=Y)
        
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
        HomePage = Home(self)
        self.PortPage = Port(self)
        CapturePage = Capture(self)
        self.AlertsPage = Alerts(self)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)
        
        HomePage.place(in_=container, x=0, y=25, relwidth=1, relheight=1)
        self.PortPage.place(in_=container, x=0, y=25, relwidth=1, relheight=1)
        CapturePage.place(in_=container, x=0, y=25, relwidth=1, relheight=1)
        self.AlertsPage.place(in_=container, x=0, y=25, relwidth=1, relheight=1)
        HomeButton = Button(self, text="Home", command=HomePage.lift)
        HomeButton.place(x=0, y=0, width=400)
        CaptureButton = Button(self, text="Capture", command=CapturePage.lift)
        CaptureButton.place(x=400, y=0, width = 400)
        AlertsButton = Button(self, text="Alerts", command=self.AlertsPage.lift)
        AlertsButton.place(x=800, y=0, width = 400)
    def LiftAlerts(self):
        self.AlertsPage.lift()
    def LiftPort(self):
        self.PortPage.lift()
        

# initialize tkinter
root = Tk()
app = Window(root)
# set window title
root.wm_title("Port Monitor")
root.wm_geometry("1200x800")
root.resizable(width=False, height=False)
# show window
root.mainloop()
