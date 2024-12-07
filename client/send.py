from vidstream import AudioSender
from threading import Thread

class VOIPSender(AudioSender):
    
    def __init__(self, ip, port=9090):
        super().__init__(host=ip, port=port)
        self.t1 = Thread(target=self.start_stream)

    def start(self):
        self.t1.start()

    def stop(self):
        self.stop_stream()
