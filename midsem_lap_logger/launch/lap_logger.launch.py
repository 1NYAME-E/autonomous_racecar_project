import os
# Making the necessary imports
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # Path to the config file in the other package
    config_path = os.path.join(
        get_package_share_directory('your_config_package_name'),
        'config',
        'race_config.yaml'  
    )

    lap_tracker_node = Node(
        package='race_monitor',
        executable='lap_tracker',
        name='lap_tracker',
        parameters=[config_path],
        output='screen'
    )

    return LaunchDescription([
        lap_tracker_node
    ])
