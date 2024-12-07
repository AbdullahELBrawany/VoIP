from client.receive import VOIPReceiver
from helpers import get_ip
from time import sleep

myIP = get_ip()
myPort = 9090 # find_free_port()

x = VOIPReceiver(myIP, myPort)
x.start()
sleep(10)
x.stop()