import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class InternSubscriber(Node):

    def __init__(self):
        super().__init__('intern_subscriber')
        self.subscription = self.create_subscription(
            String,
            'game_info',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
