import socket
from io import BytesIO
from threading import Thread

class Listener(Thread):

    def __init__(self, myIP):
        super.__init__()
        self.myIP = myIP
        self.start()

    def run(self):
        while True:
            self.sock = socket.socket()
            self.sock.bind((self.myIP, 4005))
            self.sock.listen(1)
            conn, address = self.sock.accept()
            print("Received name from:", str(address))
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            print("New user name: " + str(data))
            confirm = "Name received!"
            conn.send(confirm.encode())  # send data to the client
            conn.close()  # close the connection
            

