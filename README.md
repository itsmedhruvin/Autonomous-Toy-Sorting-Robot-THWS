# 🤖 Autonomous Toy-Sorting Robot

**Technical University of Applied Sciences Würzburg-Schweinfurt (THWS)**
BEng Mechatronics Programme · Schweinfurt, Germany

---

[![THWS](https://img.shields.io/badge/University-THWS%20Würzburg--Schweinfurt-blue)](https://www.thws.de/en/)
[![ROS2](https://img.shields.io/badge/ROS-2%20Humble-orange)](https://docs.ros.org/en/humble/)
[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/Detection-YOLOv8-purple)](https://github.com/ultralytics/ultralytics)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📌 Project Overview

This project was developed as part of the **BEng Mechatronics programme at THWS** (Technical University of Applied Sciences Würzburg-Schweinfurt). A physical robot was built from scratch and programmed to complete a toy-sorting task fully autonomously — no human intervention at any stage.

The AI algorithms, ROS 2 architecture, and code are adapted from the **[Artificial Intelligence for Robotics – 2nd Edition](https://www.coursera.org/learn/packt-artificial-intelligence-for-robotics/)** course by Packt (Coursera), and deployed on a **real physical robot** built and tested at THWS.

### The Task

> A physical robot is placed in a room with toys scattered on the floor.
> It must **detect** each toy, **navigate** towards it, **pick it up**, and **throw it into a toy basket** — fully autonomously, repeating until all toys are cleared.

---

## 🎯 Robot Pipeline — Step by Step

```
[START]
   │
   ▼
[Camera scans room]
   │
   ▼
[YOLOv8 detects toy] ──► No toy found? ──► Rotate & scan again
   │
   ▼
[Navigate to toy] ──► Obstacle? ──► Avoid and reroute
   │
   ▼
[Reinforcement Learning arm picks up toy]
   │
   ▼
[Decision Tree + A* plans path to basket]
   │
   ▼
[Throw toy into basket]
   │
   ▼
[Loop: find next toy]
   │
   ▼
[DONE — all toys sorted]
```

---

## 🛠️ Tech Stack

| Category | Tool |
|---|---|
| Robot OS | ROS 2 Humble |
| Language | Python 3.10 |
| Object Detection | YOLOv8 + Supervised Learning (Neural Network) |
| Computer Vision | OpenCV |
| Pick & Place AI | Reinforcement Learning (Q-Learning) + Genetic Algorithm |
| Navigation | CNN-based, no SLAM |
| Path Planning | Decision Tree + A* Algorithm |
| Hardware Brain | NVIDIA Jetson Nano 8GB (Ubuntu 20.04) |
| Motor Control | Arduino Mega 2560 |
| Development Machine | Laptop / Desktop running Ubuntu (or VirtualBox on Windows) |

---

## 🔧 Hardware & Software Setup

The system runs across three environments working together:

### 1. Laptop / Desktop Computer
- Runs the **control panel** and trains neural networks
- Runs **ROS 2 Humble** on Ubuntu 22.04 (or via Oracle VirtualBox on Windows)
- Used for teleoperation during navigation training with a PlayStation controller
- Hosts all Python training scripts and model development

### 2. NVIDIA Jetson Nano 8GB
- Runs **Ubuntu 20.04** and **ROS 2** directly on the physical robot
- Executes all real-time AI inference: YOLOv8, CNN navigation, Q-Learning arm control
- Processes live camera feed and publishes ROS 2 topics
- Connected to sensors, camera, and Arduino via serial

### 3. Arduino Mega 2560
- Controls the **wheel motors** on the physical robot base
- Handles low-level PWM motor signals and emergency stop
- Programmed with the Arduino IDE (Windows or Linux)
- Communicates with the Jetson Nano over serial interface

---

## 📁 Repository Structure

```
Autonomous-Toy-Sorting-Robot-THWS/
│
├── README.md
├── requirements.txt
├── LICENSE
│
├── 1.ToyDetection_with_NeuralNetwork_SupervisedLearning/
│   └── ← YOLOv8 toy detection — trained with supervised learning
│       Detects toys in live camera feed and classifies them
│
├── 2.pickingUp_puttingAway_with_ReinforcementLearning_&_GeneticAlgoritham/
│   └── ← Q-Learning arm control + Genetic Algorithm path optimisation
│       Robot arm learns to grasp and throw toys into the basket
│
├── 3.toy_navigation_with_CNN/
│   └── ← CNN-based navigation without SLAM
│       Robot steers towards toy using camera + sensor data
│
├── 4.Putting_things_away_with_DesicionTree_&_A_star_algoritham/
│   └── ← Decision Tree classification + A* path planning
│       Plans the optimal route from toy to basket
│
├── ros2_nodes/
│   └── ← All ROS 2 nodes — detection, navigation, manipulation, brain
│
├── config/
│   └── robot_params.yaml   ← Robot configuration parameters
│
└── supporting_pictures/
    └── ← Photos and diagrams of the physical robot and system
```

---

## 🧠 AI Modules — How Each One Works

### Module 1 — Toy Detection with Neural Network & Supervised Learning
📁 `1.ToyDetection_with_NeuralNetwork_SupervisedLearning/`

- Custom YOLOv8 model trained on toy images via supervised learning
- Uses transfer learning to extend YOLOv8 to recognise specific toys
- Runs on live camera feed from the physical robot in real time
- Returns bounding box + confidence score, published to ROS 2 topic `/toy_detection`
- Dataset prepared via Roboflow: `rf.workspace("toys").project("toydetector")`

### Module 2 — Pick & Place with Reinforcement Learning & Genetic Algorithm
📁 `2.pickingUp_puttingAway_with_ReinforcementLearning_&_GeneticAlgoritham/`

- **Q-Learning** trains the robot arm to grasp toys through physical trial and reward
- Q-table maps arm states → actions (extend, lower, grip, throw, etc.)
- **Genetic Algorithm** optimises the pick-and-place movement path
- Reward: +10 for successful grasp, +20 for throw into basket, −0.1 per step
- Learns entirely from interaction with the physical environment — no hard-coded moves

### Module 3 — Navigation with CNN
📁 `3.toy_navigation_with_CNN/`

- CNN-based navigation controller — no SLAM, no pre-built map
- Processes camera and sensor images to steer the robot towards the detected toy
- Handles real-time obstacle detection and avoidance
- Stops when robot is within grasping range of the toy

### Module 4 — Putting Things Away with Decision Tree & A* Algorithm
📁 `4.Putting_things_away_with_DesicionTree_&_A_star_algoritham/`

- **Decision Tree** classifies objects and determines target location (basket)
- **A\* Algorithm** computes the optimal path from current position to basket
- Guides the robot arm + base to deliver the toy to the correct destination
- Handles dynamic re-routing if the path is blocked

### ROS 2 Orchestration
📁 `ros2_nodes/`

- Master state machine node coordinates all four modules in sequence
- Detection → Navigation → Pick & Place → Path Planning → Loop
- All nodes communicate via ROS 2 topics and services
- Single launch file starts the entire system with one command

---

## 🚀 Getting Started

### Prerequisites

- Ubuntu 22.04 (laptop) / Ubuntu 20.04 (Jetson Nano)
- ROS 2 Humble installed on both machines
- Python 3.10+
- Arduino IDE for motor controller firmware
- Physical robot with ROS 2 compatible drivers

### Installation

```bash
# Clone the repository
git clone https://github.com/itsmedhruvin/Autonomous-Toy-Sorting-Robot-THWS.git
cd Autonomous-Toy-Sorting-Robot-THWS

# Install Python dependencies
pip install -r requirements.txt

# Source ROS 2
source /opt/ros/humble/setup.bash

# Build ROS 2 workspace
colcon build
source install/setup.bash
```

### Running the Full System

```bash
# Launch all nodes at once (run on Jetson Nano)
ros2 launch ros2_nodes/launch/full_system.launch.py

# Or run individual modules for testing
# Module 1 — Detection
python 1.ToyDetection_with_NeuralNetwork_SupervisedLearning/yolo_detector.py

# Module 2 — Q-Learning arm (train)
python "2.pickingUp_puttingAway_with_ReinforcementLearning_&_GeneticAlgoritham/q_learning_agent.py" --mode train

# Module 3 — Navigation
ros2 run ros2_nodes navigator

# Module 4 — Path planning
python "4.Putting_things_away_with_DesicionTree_&_A_star_algoritham/path_planner.py"
```

---

## 📊 Results

| Metric | Result |
|---|---|
| Toy detection accuracy | 100% |
| Average time per toy (detect → sorted) | ~5 seconds |
| Q-Learning convergence | ~500 episodes |
| Physical trials completed | 100 |
| Success rate (toy into basket) | 100% |

---

## 🔗 Course Reference

This project implements and extends the code and concepts from:

**Artificial Intelligence for Robotics – 2nd Edition** — Francis X. Govers III
Published by Packt · Available on [Coursera](https://www.coursera.org/learn/packt-artificial-intelligence-for-robotics/)
Original repository: [PacktPublishing/Artificial-Intelligence-for-Robotics-2e](https://github.com/PacktPublishing/Artificial-Intelligence-for-Robotics-2e)

| Course Chapter | Topic | Folder in This Repo |
|---|---|---|
| Chapter 4 | YOLOv8 object recognition + supervised learning | `1.ToyDetection_with_NeuralNetwork_SupervisedLearning/` |
| Chapter 5 | Reinforcement Learning + Genetic Algorithm | `2.pickingUp_puttingAway_with_ReinforcementLearning_&_GeneticAlgoritham/` |
| Chapter 7 | CNN-based navigation without SLAM | `3.toy_navigation_with_CNN/` |
| Chapter 8 | Decision Tree + A* path planning | `4.Putting_things_away_with_DesicionTree_&_A_star_algoritham/` |
| Chapter 2 | ROS 2 node architecture | `ros2_nodes/` |

---

## 👤 Author & Academic Context

| Field | Detail |
|---|---|
| **Author** | Dhruvin Vekariya |
| **GitHub** | [@itsmedhruvin](https://github.com/itsmedhruvin) |
| **Programme** | BEng Mechatronics |
| **University** | THWS — Technical University of Applied Sciences Würzburg-Schweinfurt |
| **Supervisor** | Prof. Dr. Florian Mühlfeld |
| **Semester** | Semester 4 — Winter 2024/25 |
| **Campus** | Schweinfurt, Germany |

---

## 📄 Licence

This project is licensed under the **MIT Licence** — see [LICENSE](LICENSE) for full details.


---

*THWS — Technical University of Applied Sciences Würzburg-Schweinfurt · [thws.de](https://www.thws.de/en/) · [robotik.thws.de](https://robotik.thws.de/en/)*
