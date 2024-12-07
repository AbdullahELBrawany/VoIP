from dns.resolver import Resolver
from helpers import ping
import socket
from copy import deepcopy
from threading import Thread

class JoinVOIPNetwork(Thread):

    def __init__(self, myName: str):
        res = Resolver()
        self.dns = deepcopy(res.nameservers)
        del res
        self.joined = False
        self.myName = myName
        self.foundDNS = self.checkAvailableDNS()
        self.retry()

    def checkAvailableDNS(self):
        availableDNS = None
        for i in self.dns:
            for n in range(0, 4):
                if ping(i)[0]:
                    availableDNS = i
                    break
            if availableDNS != None:
                break
        
        return availableDNS

    def retry(self):
        while not self.joined:
            self.start()
            self.sleep(5)
            self.sock.shutdown()

    def run(self):
        self.sock = socket.socket()
        if self.foundDNS != None:
            self.sock.connect((self.foundDNS, 4005))
            self.sock.send(self.myName.encode())  # send message
            data = self.sock.recv(1024).decode()  # receive response
            if data == "Name received!":
                self.joined = True
            else:
                print("Join failed!")

            self.sock.close()  # close the connection
        else:
            self.checkAvailableDNS()
