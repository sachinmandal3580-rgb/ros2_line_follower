#!/usr/bin/env python3
"""
Launch file for the line follower simulation.
Migrated from ROS2 Humble + Gazebo Classic → ROS2 Jazzy + Gazebo Harmonic.

Key changes:
  - gazebo_ros gzserver/gzclient → ros_gz_sim gz_sim.launch.py
  - turtlebot3_gazebo dependency removed (robot is self-contained in our model)
  - ros_gz_bridge added to forward Gz transport topics → ROS2 topics
  - GZ_SIM_RESOURCE_PATH used instead of GAZEBO_MODEL_PATH
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    pkg_follower = get_package_share_directory('follower')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # World file (now .sdf)
    world_path = os.path.join(pkg_follower, 'worlds', 'new_track.sdf')

    # Models directory — tell Gz Harmonic where to find our custom models
    models_path = os.path.join(pkg_follower, 'models')

    return LaunchDescription([
        # ── Declare arguments ──
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock',
        ),

        # ── Set GZ_SIM_RESOURCE_PATH so Gz Harmonic can find our models ──
        # (Replaces the old GAZEBO_MODEL_PATH)
        SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=models_path + ':' + os.environ.get('GZ_SIM_RESOURCE_PATH', ''),
        ),

        # ── Launch Gazebo Harmonic ──
        # Replaces the old gazebo_ros gzserver.launch.py + gzclient.launch.py
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py')
            ),
            launch_arguments={
                'gz_args': f'-r {world_path}',
            }.items(),
        ),

        # ── ros_gz_bridge: forward Gz transport topics to ROS2 ──
        # This is the KEY difference from Gazebo Classic:
        #   In Classic, plugins published directly to ROS topics.
        #   In Harmonic, sensors publish to Gz transport, and we bridge them to ROS.
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='gz_bridge',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=[
                # Clock (required for use_sim_time)
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',

                # Camera image: Gz → ROS
                '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',

                # Camera info: Gz → ROS
                '/camera/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',

                # Velocity commands: ROS → Gz
                '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',

                # Odometry: Gz → ROS
                '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',

                # IMU: Gz → ROS
                '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',

                # Joint states: Gz → ROS
                '/world/line_follower_world/model/custom_turtlebot/joint_state'
                '@sensor_msgs/msg/JointState[gz.msgs.Model',
            ],
            remappings=[
                ('/world/line_follower_world/model/custom_turtlebot/joint_state',
                 '/joint_states'),
            ],
            output='screen',
        ),

        # ── Robot State Publisher ──
        # Note: Since we use a standalone SDF model (not URDF/Xacro),
        # and the tf is published by the diff_drive plugin + bridge,
        # you may want to add a robot_state_publisher node here if you
        # need the full TF tree for RViz2. For basic line following,
        # the odom→base_footprint transform from diff_drive is sufficient.
    ])
