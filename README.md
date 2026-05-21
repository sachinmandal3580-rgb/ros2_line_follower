# ROS2 Line Follower — Jazzy + Gazebo Harmonic

> **Migrated from** ROS2 Humble + Gazebo Classic  
> **To** ROS2 Jazzy + Gazebo Harmonic (gz-sim)  
> Original repo: [gabrielnhn/ros2-line-follower](https://github.com/gabrielnhn/ros2-line-follower)

A ROS2 package that drives a differential-drive robot around a Robotrace track using camera-based P-control.

---

## Prerequisites

- **Ubuntu 24.04 (Noble)**
- **ROS2 Jazzy** — `sudo apt install ros-jazzy-desktop`
- **Gazebo Harmonic** + ROS integration — `sudo apt install ros-jazzy-ros-gz`
- **OpenCV + cv_bridge** — `sudo apt install ros-jazzy-cv-bridge python3-opencv`

<!-- ## Installation

```bash
# 1. Create workspace
mkdir -p ~/follower_ws/src
cd ~/follower_ws/src

# 2. Clone this repo
git clone <this-repo-url> ros2-line-follower-jazzy

# 3. Install dependencies
cd ~/follower_ws
source /opt/ros/jazzy/setup.bash
rosdep update
rosdep install --from-paths src --ignore-src -r -y --rosdistro jazzy

# 4. Build
colcon build --symlink-install

# 5. Source
source install/setup.bash
``` -->

## Usage

```bash
# Terminal 1: Launch the simulation
ros2 launch follower new_track.launch.py

# Terminal 2: Run the follower node
source ~/follower_ws/install/setup.bash
ros2 run follower follower_node

# Terminal 3: Start the robot
ros2 service call /start_follower std_srvs/srv/Empty

# To stop:
ros2 service call /stop_follower std_srvs/srv/Empty
```

## What Changed in the Migration

| Aspect | Humble + Gazebo Classic | Jazzy + Gz Harmonic |
|--------|------------------------|---------------------|
| **Simulator** | `gazebo` (Classic 11) | `gz sim` (Harmonic) |
| **World file** | `.world` | `.sdf` (v1.9) |
| **Launch** | `gazebo_ros` gzserver + gzclient | `ros_gz_sim` gz_sim.launch.py |
| **Sensor plugins** | `libgazebo_ros_camera.so` etc. | Built-in Gz sensors + `ros_gz_bridge` |
| **Diff-drive** | `libgazebo_ros_diff_drive.so` | `gz-sim-diff-drive-system` |
| **Joint states** | `libgazebo_ros_joint_state_publisher.so` | `gz-sim-joint-state-publisher-system` |
| **IMU** | `libgazebo_ros_imu_sensor.so` | Built-in Gz IMU sensor |
| **Material scripts** | Ogre `.material` files | PBR `<albedo_map>` in SDF |
| **Model path env** | `GAZEBO_MODEL_PATH` | `GZ_SIM_RESOURCE_PATH` |
| **Mesh URIs** | `model://turtlebot3_waffle_pi/meshes/...` | Relative `meshes/...` |
| **turtlebot3_gazebo** | Required dependency | Removed (self-contained) |

### Key Concept: The Bridge

The biggest architectural difference is that Gazebo Harmonic uses its **own transport layer** (gz-transport), separate from ROS2. Sensors (camera, IMU, etc.) publish on Gz topics, and the `ros_gz_bridge` node forwards them to ROS2 topics. In Gazebo Classic, plugins published directly to ROS topics — that pattern no longer exists.

## Troubleshooting

**Models not found?** Make sure `GZ_SIM_RESOURCE_PATH` includes the models directory. The launch file sets this automatically, but if launching manually:
```bash
export GZ_SIM_RESOURCE_PATH=~/follower_ws/install/follower/share/follower/models:$GZ_SIM_RESOURCE_PATH
```

**Camera topic not publishing?** Check that the bridge is running:
```bash
ros2 topic list | grep camera
# Should show /camera/image_raw and /camera/camera_info
```

**Black screen in Gazebo?** Gz Harmonic uses ogre2 by default. If you have GPU issues:
```bash
# Try software rendering
export LIBGL_ALWAYS_SOFTWARE=1
```

## Credits

- Original author: Gabriel Nascarella Hishida do Nascimento
- ROBOTIS CO., LTD. for the TurtleBot3 model (Apache 2.0)
- [Yapira UFPR Robotics Team](https://github.com/gabrielnhn/ros2-line-follower)
