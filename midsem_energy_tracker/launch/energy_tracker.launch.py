from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # Energy Manager Node
        Node(
            package='midsem_energy_tracker',
            executable='energy_manager',
            name='energy_manager',
            output='screen'
        ),

        # Odometry Bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/model/midsem_robot/odometry@nav_msgs/msg/Odometry[gz.msgs.Odometry'
            ],
            remappings=[
                ('/model/midsem_robot/odometry', '/odom')
            ],
            output='screen'
        )
    ])
