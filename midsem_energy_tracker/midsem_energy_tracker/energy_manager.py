# Making the necessary imports
import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.node import Node
from std_msgs.msg import Bool


class EnergyManager(Node):
    def __init__(self):
        super().__init__('energy_manager')

        # Including the necessary state variables
        self.energy_budget = 1000.0
        self.total_consumed = 0.0
        self.is_moving = False
        self.last_time = self.get_clock().now()

        self.forward_distance = 0.0
        self.backward_distance = 0.0

        # Tracking the robot's odometry
        self.last_x = None
        self.last_y = None
        self.summary_printed = False

        # Tracking all actions made by the robot 
        self.action_counts = {
            'Start Moving': 0,
            'Stop Moving': 0,
            'Move Forward (0.5 meter)': 0,
            'Move Backward (0.5 meter)': 0
        }

        self.cmd_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_callback, 10)

        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.status_pub = self.create_publisher(Bool, '/race_active', 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.calculate_energy)
        self.current_v = 0.0

        self.get_logger().info(
            "Energy has started. Waiting for movement:")

    def cmd_callback(self, msg):
        """Making updates to the linear velocity."""
        self.current_v = msg.linear.x

    def odom_callback(self, msg):
        """Tracking robot displacement using odometry."""
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y

        if self.last_x is None:
            self.last_x = x
            self.last_y = y
            return

        dx = x - self.last_x
        dy = y - self.last_y

        distance = (dx**2 + dy**2) ** 0.5

        if self.current_v > 0.01:
            self.forward_distance += distance
        elif self.current_v < -0.01:
            self.backward_distance += distance

        self.last_x = x
        self.last_y = y

    def apply_penalty(self, cost, action_name):
        """Accounting for energy deductions, updating tracking and the logger."""
        self.energy_budget -= cost
        self.total_consumed += cost
        self.action_counts[action_name] += 1
        self.get_logger().info(
            f"{action_name}: -{cost} EU. Remaining: {self.energy_budget:.1f} EU")

    def calculate_energy(self):
        """Main energy calculation loop."""
        if self.energy_budget <= 0.0:
            self.is_moving = False
            return

        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time
        currently_moving = abs(self.current_v) > 0.01

        # Including the start and stop penalties
        if currently_moving and not self.is_moving:
            self.apply_penalty(3.0, 'Start Moving')
            self.is_moving = True

        elif not currently_moving and self.is_moving:
            self.apply_penalty(1.5, 'Stop Moving')
            self.is_moving = False

        # Including the penalties as a result of distance covered
        if self.is_moving:
            # Forward distance
            while self.forward_distance >= 0.5:
                self.apply_penalty(5.0, 'Move Forward (0.5 meter)')
                self.forward_distance -= 0.5

            # Backward distance
            while self.backward_distance >= 0.5:
                self.apply_penalty(8.0, 'Move Backward (0.5 meter)')
                self.backward_distance -= 0.5

        if self.energy_budget <= 0.0 and not self.summary_printed:
            self.energy_budget = 0.0
            self.get_logger().warn("ENERGY DEPLETED! Stopping the robot.")

            # Stopping the robot
            stop_msg = Twist()
            self.cmd_pub.publish(stop_msg)

            self.print_summary()
            self.summary_printed = True

        status_msg = Bool()
        status_msg.data = self.energy_budget > 0.0
        self.status_pub.publish(status_msg)

    def print_summary(self):
        """Displaying the final output."""
        self.get_logger().info("\nENERGY SUMMARY")
        self.get_logger().info(
            f"Total Energy Consumed: {self.total_consumed:.1f} EU")
        self.get_logger().info(
            f"Unused Energy: {self.energy_budget:.1f} EU")
        self.get_logger().info("Summary of Actions Performed:")
        for action, count in self.action_counts.items():
            self.get_logger().info(f"  - {action}: {count} times")


def main(args=None):
    rclpy.init(args=args)
    node = EnergyManager()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.print_summary()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
