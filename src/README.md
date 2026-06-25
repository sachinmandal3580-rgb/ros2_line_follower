# 🤖 ROS2 Line Follower Simulation

> A TurtleBot3 Waffle Pi autonomously follows a Robotrace competition track inside Gazebo using OpenCV vision and a proportional controller — built for **ROS2 Jazzy Jalisco** on **Ubuntu 24.04**.

---

## 📋 Table of Contents

- [How It Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Running the Simulation](#running-the-simulation)
- [Controlling the Robot](#controlling-the-robot)
- [Tunable Parameters](#tunable-parameters)
- [Troubleshooting](#troubleshooting)

---

## How It Works

```
Gazebo Camera
     │
     │  /camera/image_raw  (sensor_msgs/Image)
     ▼
image_callback()
     │  cv_bridge → NumPy BGR array
     ▼
timer_callback()  [fires every 60 ms]
     │
     ├─ 1. Crop ROI  (lower 2/3, center half)
     ├─ 2. cv2.inRange()  →  binary mask
     ├─ 3. cv2.findContours()  →  contour list
     ├─ 4. cv2.moments()  →  line centroid (cx, cy)
     ├─ 5. error = cx − image_width/2
     └─ 6. angular.z = error × −KP
                │
                │  /cmd_vel  (geometry_msgs/Twist)
                ▼
          Gazebo wheels move
```

The robot detects the colored track line, measures how far it has drifted off-center (the **error**), and corrects its heading every 60 ms using a proportional gain `KP = 0.015`.

---

## Prerequisites

| Requirement | Version |
|---|---|
| **Ubuntu** | 24.04 LTS (Noble Numbat) |
| **ROS2** | Jazzy Jalisco |
| **Gazebo** | Harmonic (gz-harmonic) |
| **Python** | 3.12 (ships with Ubuntu 24.04) |

> ⚠️ ROS2 Jazzy requires Ubuntu 24.04. Do not attempt this on Ubuntu 20.04 or 22.04.

---

## Installation

### Step 1 — Install ROS2 Jazzy

```bash
# Set locale
sudo apt update && sudo apt install -y locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Add ROS2 apt repository
sudo apt install -y software-properties-common curl
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
  http://packages.ros.org/ros2/ubuntu \
  $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS2 Jazzy desktop (includes rviz2, rqt, demo nodes)
sudo apt update
sudo apt install -y ros-jazzy-desktop

# Source ROS2 in every new shell
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

### Step 2 — Install Gazebo Harmonic + ROS2 Bridge

> Jazzy pairs with **Gazebo Harmonic** (not classic Gazebo). The bridge package is `ros-jazzy-ros-gz`.

```bash
# Install Gazebo Harmonic
sudo apt install -y gz-harmonic

# Install the ROS2 ↔ Gazebo Harmonic bridge
sudo apt install -y ros-jazzy-ros-gz

# Install ros_gz_sim for launch file integration
sudo apt install -y ros-jazzy-ros-gz-sim ros-jazzy-ros-gz-bridge
```

---

### Step 3 — Install TurtleBot3 Packages

```bash
sudo apt install -y ros-jazzy-turtlebot3
sudo apt install -y ros-jazzy-turtlebot3-simulations
sudo apt install -y ros-jazzy-turtlebot3-msgs
```

---

### Step 4 — Install cv_bridge and Image Transport

```bash
sudo apt install -y ros-jazzy-cv-bridge
sudo apt install -y ros-jazzy-image-transport
sudo apt install -y ros-jazzy-image-transport-plugins
```

---

### Step 5 — Install Python Dependencies

```bash
# OpenCV for Python
pip install opencv-python

# NumPy
pip install numpy

# colcon build tool
sudo apt install -y python3-colcon-common-extensions

# rosdep
sudo apt install -y python3-rosdep
sudo rosdep init    # skip if you see "ERROR: default sources list file already exists"
rosdep update
```

---

### Step 6 — Clone and Build

```bash
# Create workspace
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# Clone the repo
git clone https://github.com/sachinmandal3580-rgb/ros2_line_follower.git

# Auto-install any remaining ROS deps declared in package.xml
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y

# Build
# --symlink-install lets you edit Python files without rebuilding
colcon build --symlink-install

# Source the workspace
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/ros2_ws/install/setup.bash
```

✅ Expected output: `Summary: 1 package finished [<time>]`

---

## Environment Setup

Set these in **every terminal** before running anything. Add to `~/.bashrc` to make them permanent.

```bash
# 1. TurtleBot3 DDS domain (standard for TurtleBot3)
export ROS_DOMAIN_ID=30

# 2. Select Waffle Pi model
export TURTLEBOT3_MODEL=waffle

# 3. Tell Gazebo where to find the custom models
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:~/ros2_ws/src/ros2_line_follower/follower/models
```

> ⚠️ On Jazzy with Gazebo Harmonic, use `GZ_SIM_RESOURCE_PATH` — not `GAZEBO_MODEL_PATH` (that was for classic Gazebo).

Add all three permanently:

```bash
echo "export ROS_DOMAIN_ID=30" >> ~/.bashrc
echo "export TURTLEBOT3_MODEL=waffle" >> ~/.bashrc
echo 'export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:~/ros2_ws/src/ros2_line_follower/follower/models' >> ~/.bashrc
source ~/.bashrc
```

---

## Running the Simulation

Open **three separate terminals**. Set the environment variables in each one (or rely on `~/.bashrc` if you added them there).

---

### Terminal 1 — Launch Gazebo

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=30
export TURTLEBOT3_MODEL=waffle
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:~/ros2_ws/src/ros2_line_follower/follower/models

ros2 launch follower new_track.launch.py
```

**What to expect:** The Gazebo Harmonic GUI opens with the Robotrace oval track. The TurtleBot3 Waffle Pi spawns at the start position. The robot sits still — the camera is publishing `/camera/image_raw` frames but nothing is processing them yet.

> ⏳ Wait until you see `[gz_ros2_control]: Loaded` in the terminal output before moving to Terminal 2.

---

### Terminal 2 — Run the Follower Node

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
export ROS_DOMAIN_ID=30

ros2 run follower follower_node
```

**What to expect:** An OpenCV window opens showing the live annotated camera feed:

| Overlay | Meaning |
|---|---|
| 🔴 Red rectangle | ROI crop boundary — the node only processes inside this box |
| 🟡 Yellow outline | Detected track line contour |
| 🟣 Pink/magenta outline | Detected lap marker contour |
| 🟢 Green dot | Computed line centroid — the robot steers toward this |

The robot is still stationary — waiting for the `/start_follower` service call.

---

### Terminal 3 — Start the Robot

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=30

ros2 service call /start_follower std_srvs/srv/Empty
```

**What to expect:** The robot starts moving immediately (within one 60 ms timer tick). Terminal 2 begins printing the control loop output:

```
Error: 14  | Angular Z: -0.21
Error: -3  | Angular Z:  0.04
Error: 8   | Angular Z: -0.12
mark_side: right
...
Finalization Process has begun!
```

---

## Controlling the Robot

### Start

```bash
ros2 service call /start_follower std_srvs/srv/Empty
```

### Stop manually (any time)

```bash
ros2 service call /stop_follower std_srvs/srv/Empty
```

### Automatic stop — lap completion

The robot stops itself after completing one full lap:

1. Right-side lap marker detected for the **2nd time** while robot is going straight
2. Terminal 2 prints `Finalization Process has begun!`
3. Robot continues for ~4 more seconds then publishes zero velocity and halts

### Emergency quit

Press `Ctrl+C` in Terminal 2. The node catches the interrupt, publishes one final zero-velocity Twist, and shuts down cleanly.

### Monitor what the robot sees (optional)

```bash
# In a separate terminal — watch the raw camera feed topic
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=30
ros2 run image_tools showimage --ros-args --remap image:=/camera/image_raw
```

### Check topic frequency (optional)

```bash
ros2 topic hz /camera/image_raw    # should be ~30 Hz
ros2 topic hz /cmd_vel             # should be ~16.7 Hz (every 60 ms)
```

---

## Tunable Parameters

All parameters are at the top of `follower/follower/follower_node.py`:

```python
MIN_AREA            = 500      # px²  — minimum contour area (noise filter)
MIN_AREA_TRACK      = 5000     # px²  — minimum area to classify as the track line
LINEAR_SPEED        = 0.2      # m/s  — forward speed while line is detected
KP                  = 1.5/100  # 0.015 — proportional gain for angular correction
LOSS_FACTOR         = 1.2      # error amplifier when line disappears (recovery spin)
TIMER_PERIOD        = 0.06     # s    — control loop period (16.7 Hz)
FINALIZATION_PERIOD = 4        # s    — extra driving time after lap marker #2
MAX_ERROR           = 30       # px   — error threshold for "going straight" check

# BGR range — adjust to match your track line color in simulation
lower_bgr_values = np.array([31, 42, 53])
upper_bgr_values = np.array([255, 255, 255])
```

| Parameter | Increase | Decrease |
|---|---|---|
| `LINEAR_SPEED` | Faster, harder to track curves | Slower, more stable on turns |
| `KP` | Sharper turns, risk of oscillation | Sluggish on tight curves |
| `LOSS_FACTOR` | More aggressive recovery spin | May not spin far enough |
| `TIMER_PERIOD` | Lower CPU load | Less responsive steering |

---

## Troubleshooting

**`Package 'follower' not found`**
```bash
source ~/ros2_ws/install/setup.bash
```

**`[Err] Model not found` in Gazebo**
```bash
export GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH:~/ros2_ws/src/ros2_line_follower/follower/models
# Then relaunch Gazebo
```

**Robot doesn't move after calling `/start_follower`**

Check that all three terminals share the same domain ID:
```bash
export ROS_DOMAIN_ID=30
```
Verify the camera is publishing:
```bash
ros2 topic hz /camera/image_raw   # must show ~30 Hz
```
Verify `/cmd_vel` is being published by the node:
```bash
ros2 topic echo /cmd_vel
```

**`No module named 'cv2'`**
```bash
pip install opencv-python
# or
sudo apt install python3-opencv
```

**`No module named 'cv_bridge'`**
```bash
sudo apt install ros-jazzy-cv-bridge
source /opt/ros/jazzy/setup.bash
```

**OpenCV window does not appear**

If running over SSH, enable X forwarding:
```bash
ssh -X user@hostname
export DISPLAY=:0
```

**`colcon build` fails with ament_python errors**
```bash
sudo apt install python3-colcon-common-extensions
sudo apt install ros-jazzy-ament-cmake python3-ament-package
```

**Robot constantly loses the line**

The BGR color range may not match the track in your environment. Print the exact BGR value of the line at a specific pixel:
```bash
python3 - << 'PYEOF'
import cv2
img = cv2.imread('/path/to/screenshot.png')
# replace 240, 320 with pixel coordinates on the line
print('BGR at pixel:', img[240, 320])
PYEOF
```
Then update `lower_bgr_values` and `upper_bgr_values` in `follower_node.py` accordingly.

---

## File Structure

```
ros2_line_follower/
├── follower/
│   ├── follower/
│   │   ├── __init__.py
│   │   └── follower_node.py          ← all vision and control logic
│   ├── launch/
│   │   └── new_track.launch.py       ← Gazebo + robot launcher
│   ├── models/
│   │   ├── robotrace_track/          ← custom Gazebo track (SDF)
│   │   └── turtlebot3_waffle_mod/    ← camera-modified robot (SDF/URDF)
│   ├── docs/
│   │   ├── about.md
│   │   └── parameters.md
│   ├── package.xml
│   ├── setup.py
│   └── setup.cfg
└── README.md
```

---

## License

MIT License — original implementation by Gabriel Nascarella Hishida do Nascimento  
TurtleBot3 models: Apache License 2.0 — ROBOTIS CO., LTD.

---

*ROS2 Jazzy Jalisco · Ubuntu 24.04 · Gazebo Harmonic · OpenCV · TurtleBot3*
