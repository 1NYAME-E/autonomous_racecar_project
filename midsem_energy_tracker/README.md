# Mid-Semester Energy Tracker (`midsem_energy_tracker`)

## Overview

This package is used to monitor and calculate the robot's energy consumption during the Autonomous Racing Challenge. It ensures the race car operates within the strict 1000 Energy Unit limit.

### Key Features

- **Odometry Tracking:** Subscribes to `/odom` to track the robot's precise distance traveled.
- [cite_start]**Dynamic Energy Calculation:** Computes energy deduction based on this rubric:
  - Move Forward (0.5m): 5 EU
  - Move Backward (0.5m): 8 EU
  - Start Moving: 3 EU
  - Stop Moving: 1.5 EU
- [cite_start]**Race Summary:** Prints a final breakdown of total energy consumed, remaining energy, and list of actions performed when the race concludes.

## Node Subscriptions & Publications

- **Subscribes to:** `/odom` (nav_msgs/Odometry) to track the position.
- **Subscribes to:** `/race_finished` (std_msgs/Bool) to trigger the final summary log.

## Usage

To run the energy manager independently:

```bash
ros2 run midsem_energy_tracker energy_manager
```
