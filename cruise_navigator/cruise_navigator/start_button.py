#!/usr/bin/env python3
import sys
import termios
import tty

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool


class StartButton(Node):
    def __init__(self):
        super().__init__('start_button')
        self.pub = self.create_publisher(Bool, '/start_trigger', 10)
        print("Wait for Simulation to load, then press 'S' to start the race.")
        self.wait_for_s()

    def wait_for_s(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                key = sys.stdin.read(1)
                if key.lower() == 's':
                    msg = Bool(data=True)
                    self.pub.publish(msg)
                    print("S key has been pressed.")
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def main():
    rclpy.init()
    node = StartButton()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
