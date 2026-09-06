#!/usr/bin/env python3
# Making the necessary imports
import math

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool

# All speeds used
CRUISE_SPEED = 0.35    
CORNER_SPEED = 0.22   
EMERGENCY_SPEED = 0.10 

# Senitivity for steering
STEER_GAIN = 2.2       
MAX_STEER = 2.0        

# Wall following
WALL_SETPOINT = 0.60   
WALL_TOLERANCE = 0.05   

# Distance thresholds 
FRONT_STOP_DIST = 0.65  
FRONT_LEFT_DIST = 0.85  

# Laser scan zones 
FRONT_HALF_DEG = 10    
FL_LOW_DEG = 10         
FL_HIGH_DEG = 45        
LEFT_LOW_DEG = 45       
LEFT_HIGH_DEG = 110

WARMUP_REQUIRED = 200  

CMD_TOPIC = '/cmd_vel' 
SCAN_TOPIC = '/scan'
RACE_TOPIC = '/race_active'



def _zone_min(ranges, angle_min_rad, angle_increment_rad, low_deg, high_deg):
    low_idx = max(
        0, round((math.radians(low_deg) - angle_min_rad) / angle_increment_rad))
    high_idx = min(len(ranges) - 1, round((math.radians(high_deg) -
                   angle_min_rad) / angle_increment_rad))
    if low_idx > high_idx:
        return float('inf')
    valid = [r for r in ranges[low_idx: high_idx + 1]
             if not math.isinf(r) and not math.isnan(r) and r > 0.05]
    return min(valid) if valid else float('inf')


class WallFollower(Node):

    def __init__(self):
        super().__init__('wall_follower')

        self._pub = self.create_publisher(Twist, CMD_TOPIC, 10)
        self._scan_sub = self.create_subscription(
            LaserScan, SCAN_TOPIC, self._scan_callback, 10)
        self._race_sub = self.create_subscription(
            Bool, RACE_TOPIC, self._race_status_callback, 10)

        self._ranges = []
        self._angle_min = 0.0
        self._angle_inc = 0.0
        self._scan_ready = False
        self.race_active = True
        self.ready_to_move = False
        self.warmup_ticks = 0

        self._timer = self.create_timer(0.05, self._control_loop)
        self.get_logger().info('WallFollower started.')

    def _race_status_callback(self, msg: Bool):
        self.race_active = msg.data

    def _scan_callback(self, msg: LaserScan):
        self._ranges = list(msg.ranges)
        self._angle_min = msg.angle_min
        self._angle_inc = msg.angle_increment
        self._scan_ready = True

    def _control_loop(self):
        if not self._scan_ready:
            return

        if not self.race_active:
            self._publish(0.0, 0.0)
            return

        # Waiting for a moment
        if not self.ready_to_move:
            self.warmup_ticks += 1
            if self.warmup_ticks >= WARMUP_REQUIRED:
                self.ready_to_move = True
                self.get_logger().info('Ready to go now')
            return

        front = _zone_min(self._ranges, self._angle_min,
                          self._angle_inc, -FRONT_HALF_DEG, FRONT_HALF_DEG)
        front_left = _zone_min(self._ranges, self._angle_min,
                               self._angle_inc, FL_LOW_DEG, FL_HIGH_DEG)
        left = _zone_min(self._ranges, self._angle_min,
                         self._angle_inc, LEFT_LOW_DEG, LEFT_HIGH_DEG)

        speed = CRUISE_SPEED
        steer = 0.0

        # Something directly in front
        if front < FRONT_STOP_DIST:
            speed = EMERGENCY_SPEED
            steer = -MAX_STEER 

        # INNER CORNER
        elif front_left < FRONT_LEFT_DIST:
            speed = CORNER_SPEED
            steer = -MAX_STEER * 0.7 

        # PROPORTIONAL WALL FOLLOWING
        else:
            error = WALL_SETPOINT - left

            if abs(error) > WALL_TOLERANCE:
                steer = error * STEER_GAIN
            else:
                steer = 0.0

        steer = max(min(steer, MAX_STEER), -MAX_STEER)
        self._publish(speed, steer)

    def _publish(self, speed, steer):
        msg = Twist()
        msg.linear.x = float(speed)
        msg.angular.z = float(steer)
        self._pub.publish(msg)

    _last_log: float = 0.0

    def _log(self, text: str):
        now = self.get_clock().now().nanoseconds * 1e-9
        if now - self._last_log >= 1.0:
            self.get_logger().info(text)
            self._last_log = now


def main(args=None):
    rclpy.init(args=args)
    node = WallFollower()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
