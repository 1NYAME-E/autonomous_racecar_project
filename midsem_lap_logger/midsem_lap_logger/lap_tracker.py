#!/usr/bin/env python3
# Making the necessary imports
import time

import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from std_msgs.msg import Bool


class LapTracker(Node):
    def __init__(self):
        super().__init__('lap_tracker')

        # The subscribers
        self.odom_sub = self.create_subscription(
            Odometry, '/odom', self.odom_cb, 10)

        # The publishers
        self.race_active_pub = self.create_publisher(Bool, '/race_active', 10)
        self.cmd_vel_pub = self.create_publisher(
            Twist, '/cmd_vel', 10) 

        # The goal line parameters
        self.start_x = -0.25
        self.start_y = 1.3

        # Racing state
        self.lap_count = 0
        self.max_laps = 3
        self.start_time = None
        self.lap_start_ts = None
        self.is_finished = False  

        self.last_x = None
        self.has_cleared_line = False

        self.last_lap_time = 0.0

        self.min_dist_to_arm = 1.0
        self.y_threshold = 1.5

        self.get_logger().info(
            "Lap tracker is now ready")

    # Stop if the race is over 
    def odom_cb(self, msg):
        if self.is_finished:
            return  

        curr_x = msg.pose.pose.position.x
        curr_y = msg.pose.pose.position.y

        if self.last_x is None:
            self.last_x = curr_x
            return

        if self.start_time is None and abs(curr_x - self.last_x) > 0.01:
            self.start_time = time.time()
            self.lap_start_ts = self.start_time
            self.get_logger().info("Timer Activated")

        if not self.has_cleared_line and abs(curr_x - self.start_x) > self.min_dist_to_arm:
            self.has_cleared_line = True

        if self.has_cleared_line:
            crossed_x = (self.last_x <= self.start_x < curr_x) or (
                self.last_x >= self.start_x > curr_x)
            within_y_gate = abs(curr_y - self.start_y) < self.y_threshold

            now = time.time()
            if crossed_x and within_y_gate and (now - self.last_lap_time > 5.0):

                if self.start_time is None:
                    self.start_time = now
                    self.lap_start_ts = now

                self.lap_count += 1
                self.has_cleared_line = False 
                self.last_lap_time = now

                lap_time = now - self.lap_start_ts
                total_time = now - self.start_time
                self.lap_start_ts = now

                self.get_logger().info(f"✅ LAP {self.lap_count} COMPLETE!")
                self.get_logger().info(
                    f" Lap Time: {lap_time:.2f}s | Total Race Time: {total_time:.2f}s")

                if self.lap_count >= self.max_laps:
                    self.finish_race(total_time)

        self.last_x = curr_x

    def finish_race(self, final_time):
        self.is_finished = True

        active_msg = Bool()
        active_msg.data = False
        self.race_active_pub.publish(active_msg)

        # Command the robot to stop immediately
        stop_msg = Twist()
        stop_msg.linear.x = 0.0
        stop_msg.angular.z = 0.0
        for _ in range(5):
            self.cmd_vel_pub.publish(stop_msg)
            time.sleep(0.1)

        self.get_logger().info(" 3 LAPS COMPLETED")
        self.get_logger().info(f" Final Race Time: {final_time:.2f}s")


def main(args=None):
    rclpy.init(args=args)
    node = LapTracker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
