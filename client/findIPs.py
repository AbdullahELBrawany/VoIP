from helpers import ping
import socket
from threading import Thread

class finder(Thread):

    def __init__(self, myIP, dnsEnabled=False):
        super().__init__()
        self.networks = ["10.0.0.", "20.0.0."]
        self.names = {}
        self.myIP = myIP
        self.dnsEnabled = dnsEnabled
        self.running = True
        self.start()

    def run(self):
        while self.running:
            for i in range(2, 255):
                if not self.running:
                    break
                for n in range(0, 2):
                    if not self.running:
                        break
                    res = ping(self.networks[n]+str(i))
                    if res[0] and res[1] != self.myIP:
                        if self.dnsEnabled:
                            name = socket.gethostbyaddr(res[1])
                        else:
                            name = res[1]
                        if name not in self.names:
                            self.names[name] = res[1]
