"""
ros2_nodes/robot_brain.py

Project: Autonomous Toy-Sorting Robot
Author: Dhruvin Vekariya
Accosiation: Technical University of Applied Science Würzburg-Schweinfurt


Master orchestration node. Coordinates the full pipeline:
  Detection → Navigation → Manipulation → Loop
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String
from geometry_msgs.msg import Point
import time


class RobotState:
    SCANNING = "scanning"
    NAVIGATING = "navigating"
    MANIPULATING = "manipulating"
    DONE = "done"


class RobotBrain(Node):
    """
    Master state machine that coordinates:
    1. Toy detection
    2. Navigation to toy
    3. Pick and throw (Q-Learning arm)
    4. Loop back to scanning
    """

    def __init__(self):
        super().__init__("robot_brain")
        self.get_logger().info("Robot Brain started — THWS Toy-Sorting Robot")

        self.state = RobotState.SCANNING
        self.toy_found = False
        self.navigation_done = False
        self.manipulation_done = False
        self.toys_sorted = 0

        # Subscribers
        self.create_subscription(Bool, "/toy_found", self.toy_found_cb, 10)
        self.create_subscription(Bool, "/navigation_done", self.nav_done_cb, 10)
        self.create_subscription(Bool, "/manipulation_done", self.manip_done_cb, 10)

        # Publishers — commands to other nodes
        self.start_nav_pub = self.create_publisher(Bool, "/start_navigation", 10)
        self.start_manip_pub = self.create_publisher(Bool, "/start_manipulation", 10)
        self.state_pub = self.create_publisher(String, "/robot_state", 10)

        # Main loop at 2Hz
        self.create_timer(0.5, self.state_machine)
        self.get_logger().info("State machine running. Waiting for toy detection...")

    def toy_found_cb(self, msg):
        self.toy_found = msg.data

    def nav_done_cb(self, msg):
        self.navigation_done = msg.data

    def manip_done_cb(self, msg):
        self.manipulation_done = msg.data

    def state_machine(self):
        """Main state machine — transitions between robot states."""

        # Publish current state for monitoring
        state_msg = String()
        state_msg.data = self.state
        self.state_pub.publish(state_msg)

        if self.state == RobotState.SCANNING:
            if self.toy_found:
                self.get_logger().info("Toy detected! Starting navigation...")
                self._publish_bool(self.start_nav_pub, True)
                self.navigation_done = False
                self.state = RobotState.NAVIGATING

        elif self.state == RobotState.NAVIGATING:
            if self.navigation_done:
                self.get_logger().info("At toy position! Starting manipulation...")
                self._publish_bool(self.start_manip_pub, True)
                self.manipulation_done = False
                self.state = RobotState.MANIPULATING

        elif self.state == RobotState.MANIPULATING:
            if self.manipulation_done:
                self.toys_sorted += 1
                self.get_logger().info(
                    f"Toy sorted! Total sorted: {self.toys_sorted}. Scanning for next toy..."
                )
                self.toy_found = False
                self.navigation_done = False
                self.manipulation_done = False
                self.state = RobotState.SCANNING

    def _publish_bool(self, publisher, value):
        msg = Bool()
        msg.data = value
        publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = RobotBrain()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info(f"Shutting down. Toys sorted this session: {node.toys_sorted}")
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
