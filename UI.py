from tkinter import *
from tkintertable import *
import PacketSniffer


class Page(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
    def show(self):
        self.lift()

class Home(Page):
    def __init__(self, master=None):
        Page.__init__(self, master)
        AlertsPage = Alerts(self)
        PortTable = Treeview(self)
        PortTable['columns'] = ('Application', 'Protocol', 'Sending(B/sec)', 'Recieving(B/sec)', 'View')
        PortTable.heading("#0", text='Port No.', anchor='w')
        PortTable.column("#0", anchor="w", width=30)
        PortTable.heading('Application', text='Application')
        PortTable.column('Application', anchor='center', width=100)
        PortTable.heading('Protocol', text='Protocol')
        PortTable.column('Protocol', anchor='center', width=100)
        PortTable.heading('Sending(B/sec)', text='Sending(B/sec)')
        PortTable.column('Sending(B/sec)', anchor='center', width=100)
        PortTable.heading('Recieving(B/sec)', text='Recieving(B/sec)')
        PortTable.column('Recieving(B/sec)', anchor='center', width=100)
        PortTable.heading('View', text='View')
        PortTable.column('View', anchor='center', width=30)
        PortTable.grid(sticky = (N, W, E))
        self.treeview = PortTable
        Label(self, text='Number of Alerts: ', borderwidth=1).grid(sticky=(S, W), padx=100, pady=0)
        Label(self, text='Highest Priority: ', borderwidth=1).grid(sticky=(S, W), padx=100, pady=50)
        Button(self, text='Go To Alerts').grid(sticky=(S, W), padx=200, pady=30)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        
        

        
        
class Port(Page):
    def __init__(self, master=None):
        Page.__init__(self, master)

class Capture(Page):
    def __init__(self, master=None):
        Page.__init__(self, master)
        CaptureTable = Treeview(self)
        CaptureTable['columns'] = ['Source', 'Destination', 'Protocol', 'Information']
        CaptureTable['show'] = 'headings'
        CaptureTable.heading('Source', text='Source')
        CaptureTable.column('Source', anchor="w", width=100)
        CaptureTable.heading('Destination', text='Destination')
        CaptureTable.column('Destination', anchor='center', width=100)
        CaptureTable.heading('Protocol', text='Protocol')
        CaptureTable.column('Protocol', anchor='center', width=100)
        CaptureTable.heading('Information', text='Information')
        CaptureTable.column('Information', anchor='e', width=100)
        CaptureTable.grid(sticky = (N,E,S,W))
        self.treeview = CaptureTable
        
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)


        Array = PacketSniffer.CapturePackets(100)
        index = iid = 0
        for row in Array:
            CaptureTable.insert("", index, iid, values=row)
            index = iid = index + 1
        
        
class Alerts(Page):
    def __init__(self, master=None):
        Page.__init__(self, master)
        AlertTable = Treeview(self)
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
        AlertTable.grid(sticky = (N,E,S,W))
        self.treeview = AlertTable
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)
        HomePage = Home(self)
        PortPage = Port(self)
        CapturePage = Capture(self)
        AlertsPage = Alerts(self)

        buttonframe = Frame(self)
        container = Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)
        
        HomePage.place(in_=container, x=0, y=25, relwidth=1, relheight=1)
        PortPage.place(in_=container, x=0, y=25, relwidth=1, relheight=1)
        CapturePage.place(in_=container, x=0, y=25, relwidth=1, relheight=1)
        AlertsPage.place(in_=container, x=0, y=25, relwidth=1, relheight=1)
        HomeButton = Button(self, text="Home", command=HomePage.lift)
        HomeButton.place(x=0, y=0)
        CaptureButton = Button(self, text="Capture", command=CapturePage.lift)
        CaptureButton.place(x=74, y=0)
        AlertsButton = Button(self, text="Alerts", command=AlertsPage.lift)
        AlertsButton.place(x=147, y=0)
        
    
        

# initialize tkinter
root = Tk()
app = Window(root)

# set window title
root.wm_title("Port Monitor")
root.wm_geometry("800x400")
# show window
root.mainloop()
