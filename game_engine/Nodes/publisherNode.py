import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class Publisher(Node):

    def __init__(self, node_name, topic):
        super().__init__(node_name)
        self.publisher_ = self.create_publisher(String, topic, 10)
        
    def send(self, key):
        msg = String()
        msg.data = key
        self.publisher_.publish(msg)

    def get_subscription_count(self):
        return self.publisher_.get_subscription_count()
