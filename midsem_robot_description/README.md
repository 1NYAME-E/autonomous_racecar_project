# Mid-Semester Robot Description (`midsem_robot_description`)

## Overview

This package contains the physical description of the racing robot. It defines the robot's URDF using Xacro macros and spawns the robot in Gazebo.

### Key Features

- **Ackermann Steering Architecture:** Implements front-wheel steering and rear-wheel drive.
- **Dynamic Spawning:** The `spawn.launch.py` automatically parses track YAML configuration files to determine the exact `[X, Y, Yaw]` starting coordinates to spawn at the given spawn position.
- **Sensor Suite:** \* GPU LiDAR (`scan`) is used for wall and obstacle detection.
  - RGB Camera (`camera/image_raw`) for traffic sign recognition.
- **Gazebo Integration:** Fully integrated with `ros_gz_bridge` for parameter sharing between ROS 2 and Gazebo.

## Package Structure

- `/urdf`: Contains all `.xacro` files (`robot_core`, `lidar`, `camera`, `inertial_macros`).
- `/launch`:
  - `rsp.launch.py`: Starts the `robot_state_publisher`.
  - `spawn.launch.py`: Reads the YAML configuration and spawns the robot into the Gazebo world.
- `/config`: Contains the `bridge_parameters.yaml` which help ROS2 communicate with Gazebo.

## Usage

To spawn the robot into an active Gazebo world, run:

```bash
ros2 launch midsem_robot_description spawn.launch.py
```


To spawn the robot into an active Gazebo world, run:

```bash
ros2 launch midsem_robot_description spawn.launch.py
