from .Nodes import *

def main(args=None):

    rclpy.init(args=args)

    intern_subscriber = InternSubscriber()

    rclpy.spin(intern_subscriber)


    intern_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()