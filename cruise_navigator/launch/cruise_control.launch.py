from launch import LaunchDescription
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node


def generate_launch_description():

    initial_turn = Node(
        package='cruise_navigator',
        executable='initial_turn',
        name='initial_turn',
        output='screen'
    )

    wall_follower = Node(
        package='cruise_navigator',
        executable='wall_follower',
        name='wall_follower',
        output='screen'
    )

    delayed_wall_follower = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=initial_turn,
            on_exit=[wall_follower],
        )
    )

    return LaunchDescription([
        initial_turn,
        delayed_wall_follower
    ])
