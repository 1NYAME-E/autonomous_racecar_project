# Making the necessary imports
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():

    # Tracking the package
    pkg_name = "midsem_robot_description"
    pkg_path = get_package_share_directory(pkg_name)

# Tracking the xacro file for the robot description
    xacro_file = os.path.join(pkg_path, "urdf", "robot.urdf.xacro")

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )

    return LaunchDescription([
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            output="screen",
            parameters=[{"robot_description": robot_description}]
        )
    ])
