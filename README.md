# ROBOTRACE — Autonomous Vision-Based Line Following Challenge

---

## Problem Statement

In modern robotics, one of the fundamental capabilities of autonomous systems is visual navigation without external positioning systems.

From warehouse robots to self-driving cars, machines must be able to:

> perceive their environment → interpret structure → take corrective action in real time

This challenge simulates that exact problem in a controlled environment.

---

## The Story: A Robot Without a Map

Somewhere inside a quiet simulated world, a robot opens its eyes for the first time.

It doesn't know where it is. It doesn't know where it's going.

There is no map, no GPS, no human guidance. It has been placed on a track it has never seen.

All it has is one sense:

> A single forward-facing camera.

At first, everything is just noise. But gradually, a pattern emerges — a line on the ground.

That line becomes its only guide.

The robot repeatedly asks:

> Am I still on the line — and if not, how do I get back?

---

## Objective

Design and implement an autonomous system for real-time vision-based line following in ROS2 and Gazebo.

The robot must:
- Detect the track
- Stay centered on it
- Recover from drift or loss of vision
- Identify markers on the track
- Complete a full lap
- Stop safely at the end

---

## Core Idea

Camera Input → OpenCV Processing → Error Computation → Control Output → Robot Motion

The system continuously minimizes deviation from the track center using feedback control.

---

## System Overview

### Robot (SDF Model)

A simulated differential-drive robot in Gazebo.

Features:
- Differential drive base
- RGB camera
- Physics-based motion
- Diff-drive plugin control

Purpose:
Defines physical behavior in simulation (movement, camera view, stability).

---

### Follower Node (Brain)

A ROS2 Python node responsible for:
- Reading camera images
- Detecting track using OpenCV
- Computing error from center
- Generating motion commands
- Handling recovery and completion logic

---

## Perception Pipeline

Raw Image → ROI → Color Threshold → Contours → Centroid → Error

Output:
- Error = distance from track center

---

## Control Strategy

error = center_of_image - center_of_line  
angular.z = -Kp * error  
linear.x = constant speed

---

## Failure Handling

When line is lost:
1. Use last known error
2. Amplify correction
3. Reduce forward motion
4. Search for track again

---

## Mission Completion

- Detect markers
- Track laps
- Confirm completion
- Execute safe shutdown

---

## WHAT YOU NEED TO CHANGE

You will complete TODOs across 4 files:

---

### 1. follower_node.py (Brain)

Vision:
- ROI cropping
- Color thresholding
- Contour detection
- Centroid extraction
- Marker detection

Control:
- Error computation
- Recovery behavior
- PID/proportional control
- Speed tuning

Logic:
- Lap counting
- Completion detection
- Safe shutdown

---

### 2. custom_turtlebot3.sdf (Robot)

Camera:
- Position and tilt
- Field of View
- Update rate
- Noise model

Physics:
- Wheel radius
- Wheel separation
- Friction tuning
- Contact stability

Control plugin:
- Diff-drive parameters

---

### 3. world.sdf (Environment)

- Robot spawn position (x, y)
- Initial yaw orientation

Why:
Controls whether robot can even see the track properly.

---

### 4. setup.py (ROS2 Build)

Add console script entry:

follower = follower.<your_file>:main

Without this:
- ros2 run will not work
- node will not start

---

## Bonus Challenges

- PID control upgrade
- Live telemetry dashboard
- Adaptive speed control
- Custom track design

---

## Deliverables

1. Demo video:
- Startup
- Tracking
- Recovery
- Full lap
- Shutdown

2. GitHub repo:
- Source code
- SDF models
- Launch files
- README

3. Report:
- Design
- Vision pipeline
- Control strategy
- Tuning process

---

## Final Message

This project is a full autonomy loop:

See → Understand → Act → Recover → Improve

If completed successfully, you have built a working autonomous system.
