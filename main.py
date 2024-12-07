from helpers import get_ip
from sys import exit, argv
from client.clientWindow import window
from easygui import enterbox

myIP = get_ip()
print("IP:",myIP)
myPort = 9090 # find_free_port()
print("Port:",myPort)
otherNetwork = ""

if "20.0.0." not in myIP and "10.0.0." not in myIP:
    print("PLEASE ENTER ONE OF THE LOCAL ROUTERS!!!")
    exit()

if __name__ == "__main__":
    name = ""
    while name.strip() == "":
        name = enterbox("Please enter your name: ")
    app = window(myName=name, myIP=myIP)
    app.mainloop()
