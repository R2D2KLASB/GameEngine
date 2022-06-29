import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class Listener(Node):
    def __init__(self, node_name, topic, queue):
        super().__init__(node_name)
        self.subscription = self.create_subscription(String, topic, self.listener_callback,10)
        self.queue = queue

    def listener_callback(self, msg):
        self.queue.add(msg.data)




