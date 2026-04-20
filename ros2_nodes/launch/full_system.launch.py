"""
ros2_nodes/launch/full_system.launch.py
THWS Toy-Sorting Robot Project

Launches all ROS 2 nodes together:
  - robot_brain      (master orchestration)
  - toy_detector     (YOLOv8 detection)
  - navigator        (movement control)
  - arm_controller   (Q-Learning manipulation)

Usage:
  ros2 launch toy_sorting_robot full_system.launch.py
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import LogInfo


def generate_launch_description():
    return LaunchDescription([

        LogInfo(msg="=== THWS Toy-Sorting Robot — Starting All Nodes ==="),

        Node(
            package="toy_sorting_robot",
            executable="robot_brain",
            name="robot_brain",
            output="screen",
        ),

        Node(
            package="toy_sorting_robot",
            executable="toy_detector",
            name="toy_detector",
            output="screen",
        ),

        Node(
            package="toy_sorting_robot",
            executable="navigator",
            name="navigator",
            output="screen",
        ),

        Node(
            package="toy_sorting_robot",
            executable="arm_controller",
            name="arm_controller",
            output="screen",
        ),

        LogInfo(msg="=== All nodes launched. Robot is running. ==="),
    ])
