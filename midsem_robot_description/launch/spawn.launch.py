# Making the necessary imports
import os

import yaml
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    package_name = 'midsem_robot_description'
    ashbot_world_pkg = get_package_share_directory('ashbot_world')

    # Path to the race track's .yaml file
    yaml_file_path = os.path.join(
        ashbot_world_pkg, 'config', 'race_track.yaml')

    with open(yaml_file_path, 'r') as f:
        config_data = yaml.safe_load(f)

    # Extracting starting position from the list
    coords = config_data.get('start_coordinate', [0.0, 0.0, 0.0])
    spawn_x = str(coords[0])
    spawn_y = str(coords[1])
    spawn_yaw = str(coords[2])

    # Including the existing launch file (Robot State Publisher)
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(
                package_name), 'launch', 'rsp.launch.py'
        )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Path to the racing world
    world_file = os.path.join(
        ashbot_world_pkg, 'worlds', 'race_track.world')

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory(
                'ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': f'-r -v 4 {world_file}'}.items(),
    )

    # Spawning the robot
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'midsem_robot',
            '-x', spawn_x,
            '-y', spawn_y,
            '-z', '0.1',
            '-Y', spawn_yaw
        ],
        output='screen'
    )

    # Bridging the parameters
    bridge_params = os.path.join(get_package_share_directory(
        package_name), 'config', 'bridge_parameters.yaml')

    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            '--ros-args',
            '-p', f'config_file:={bridge_params}',
        ]
    )

    # The execution
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
        ros_gz_bridge,
    ])
