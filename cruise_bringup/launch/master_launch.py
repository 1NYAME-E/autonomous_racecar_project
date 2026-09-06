import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    # Spawning the world
    spawn_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('midsem_robot_description'),
                'launch', 'spawn.launch.py'
            )
        )
    )

    # Managing the energy
    energy_node = Node(
        package='midsem_energy_tracker',
        executable='energy_manager',
        name='energy_manager',
        output='screen'
    )

    # Waiting to ensure Gazebo is fully loaded
    delayed_race_nodes = TimerAction(
        period=12.0, 
        actions=[
            Node(
                package='cruise_navigator',
                executable='wall_follower',
                name='wall_follower',
                output='screen'
            ),
            Node(
                package='midsem_lap_logger',
                executable='lap_tracker',
                name='lap_tracker',
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        spawn_launch,
        energy_node,
        delayed_race_nodes
    ])
