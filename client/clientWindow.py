import tkinter as tk
from client.findIPs import finder
from client.receive import VOIPReceiver
from client.send import VOIPSender
from client.join import JoinVOIPNetwork
from helpers import ping

class window(tk.Tk):

    def __init__(self, myName, myIP, myPort=9090):
        super().__init__()
        self.dnsEnabled = False
        self.myIP = myIP
        if self.dnsEnabled:
            self.joiner = JoinVOIPNetwork(myName=myName)
        self.searcher = finder(myIP=self.myIP, dnsEnabled=self.dnsEnabled)
        self.receiver = VOIPReceiver(ip=myIP, port=myPort)
        self.receiver.start()
        self.sender = None
        self.init_UI()
        

    def init_UI(self):
        self.title("VOIP Project")
        self.title_label = tk.Label(self, text="Choose callee",  font=("Arial", 14))
        self.title_label.pack(pady=10)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.selected_option = tk.StringVar(value="none")
        self.radio_button_array = []

        self.refreshRadio()

        self.refresh_button = tk.Button(self, text="Refresh list", width=15, command=self.refreshRadio)
        self.refresh_button.pack(pady=10)

        self.call_button = tk.Button(self, text="Call", width=15, command=lambda: self.startSender(self.selected_option.get()))
        self.call_button.pack(pady=10)

    def on_closing(self):
        self.searcher.running = False
        self.receiver.stop()
        if self.sender != None:
            self.sender.stop()
        self.destroy()

    def deleteRadio(self):
        for i in reversed(self.radio_button_array):
            i.destroy()
            del i
        self.update()
        self.radio_button_array = []

    def refreshRadio(self):
        if len(self.radio_button_array) != 0:
            self.deleteRadio()
        
        for name, ip in self.searcher.names.items():
            self.radio_button = tk.Radiobutton(self, text=f"{name}", variable=self.selected_option, value=f"{ip}")
            self.radio_button.pack(anchor=tk.W)
            self.radio_button_array.append(self.radio_button)
        self.update()

    def startSender(self, ip, port=9090):
        if ip == "none":
            return
        self.deleteRadio()
        if ping(ip)[0]:
            self.call_button.configure(text="End Call", command=self.endSender)
            self.update()
            self.sender = VOIPSender(ip=ip, port=port)
            self.sender.start()
        else:
            print("IP not found!")

    def endSender(self):
        self.sender.stop()
        self.refreshRadio()
        self.call_button.configure(text="Call", command=lambda: self.startSender(self.selected_option.get()))
        self.update()
        


