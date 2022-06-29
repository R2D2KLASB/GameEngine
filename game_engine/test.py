from .Nodes import *
import rclpy
import threading

def reading(queue):
    while True:
        print(queue.read(wait=True))

def main(args=None):
    rclpy.init()
    queue = Queue()
    extern_listener = Listener('extern_listener', 'game_info/B', queue)
    t1 = threading.Thread(target=rclpy.spin, args=(extern_listener,))
    t2 = threading.Thread(target=reading, args=(queue,))
    t1.start()
    t2.start()