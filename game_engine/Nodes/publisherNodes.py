import rclpy
from rclpy.node import Node

from std_msgs.msg import String

class InternPublisher(Node):

    def __init__(self):
        super().__init__('inter_publisher')
        self.publisher_ = self.create_publisher(String, 'game_info', 10)

    def send(self, key):
        msg = String()
        msg.data = key
        self.publisher_.publish(msg)
