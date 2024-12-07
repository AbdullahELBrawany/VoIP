from vidstream import AudioReceiver
from threading import Thread

class VOIPReceiver(AudioReceiver):

    def __init__(self, ip, port=9090):
        super().__init__(host=ip, port=port)
        self.t1 = Thread(target=self.start_server)

    def start(self):
        self.t1.start()

    def stop(self):
        self.stop_server()
