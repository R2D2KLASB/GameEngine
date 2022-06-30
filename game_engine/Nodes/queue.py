import time

class Queue():
    def __init__(self):
        self.queue = []
    
    def add(self, key):
        self.queue += [key]

    def wait(self):
        while not self.queue:
            time.sleep(0.1)

    def read(self, wait=False):
        if not self.queue and wait == False:
            return False
        elif wait:
            self.wait()
        key = self.queue[0]
        # FIX VOOR MATRIX
        if key == 'ok':
            self.queue.pop(0)
            return self.read(wait)
        self.queue.pop(0)
        return key
    
    def read_all(self, wait=False):
        if not self.queue and wait == False:
            return False
        elif wait:
            self.wait()
        keys = self.queue
        self.queue = []
        return keys