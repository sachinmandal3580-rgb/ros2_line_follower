# 🏁 ROBOTRACE — Autonomous Vision-Based Line Following Challenge

---

## 🚀 Problem Statement

In modern robotics, one of the fundamental capabilities of autonomous systems is **visual navigation without external positioning systems**.

From warehouse robots to self-driving cars, machines must be able to:

> perceive their environment → interpret structure → take corrective action in real time

This challenge simulates that exact problem in a controlled environment.

---

## 📖 The Story: A Robot Without a Map

Somewhere inside a quiet simulated world, a robot opens its eyes for the first time.

It doesn't know where it is.

It doesn't know where it's going.

There is no map loaded into its memory. No GPS satellite watching from above. No human standing nearby to guide it. It has been placed on a track it has never seen, in a world it knows nothing about — and it is completely on its own.

All it has is one sense:

> 👁️ A single forward-facing camera.

In the first few milliseconds, the world makes no sense at all. Just pixels. Noise. Motion blur. A blur of color with no meaning.

But somewhere in that chaos — there's a pattern. A shape. A line, curving ahead into the unknown.

And slowly, frame by frame, the robot starts to understand it.

That line becomes its compass. Its rulebook. Its entire universe.

Every second, it has to ask itself the same question, over and over again:

> *"Am I still on the line — and if not, how do I get back?"*

That single question — asked thousands of times per minute — is the heartbeat of this entire challenge. Get it right, and the robot glides smoothly around every curve. Get it wrong, and it drifts, wobbles, and eventually loses the track entirely.

This is your robot's story to write. You are not just writing code — you are teaching a machine how to *see*, how to *think*, and how to *recover* when things go wrong. That's the real magic of robotics: it's not about perfection, it's about resilience.

So — can you build a robot that never gives up, even when it loses sight of the path?

---

## 🤖 Objective

Design and implement an autonomous system that enables a robot to perform **real-time vision-based line following in simulation using ROS2 and Gazebo**.

The robot must:

- Detect the track
- Stay centered on it
- Recover from drift or loss of vision
- Identify special markers on the track
- Complete a full lap autonomously
- Stop safely upon mission completion

---

## 🧠 Core Idea: The Robotics Loop

```
Camera Input → OpenCV Processing → Error Computation → Control Output → Robot Motion
```

At its core, the robot continuously minimizes deviation from the center of the track using feedback control.

---

## ⚙️ System Overview

This project is built using two tightly connected components:

### 🤖 1. Custom Robot (SDF Model) — The Body

A physically simulated differential-drive robot inside Gazebo.

**🔧 Features:**

- Differential drive base (2 wheels + casters)
- Forward-facing RGB camera
- Physics-based inertia and friction
- Gazebo diff-drive plugin for motion control

**🎯 Purpose:**

This defines the physical behavior of the robot in simulation.

It determines:

- Stability
- Turning behavior
- Camera viewpoint
- Real-world realism

### 🧠 2. Follower Node — The Brain

A Python-based ROS2 node that acts as the robot's intelligence.

It is responsible for:

- Reading camera images
- Detecting the track using OpenCV
- Computing deviation from center
- Generating motion commands
- Handling recovery and completion logic

---

## 👁️ Perception Pipeline

Each frame is processed as:

```
Raw Camera Image
   ↓
Region of Interest (ROI)
   ↓
Color Thresholding (track segmentation)
   ↓
Contour Detection
   ↓
Centroid Extraction
   ↓
Error Computation
```

The output is a single value:

> `error` = how far the robot is from the center

---

## ⚖️ Control Strategy

The robot uses proportional control:

```python
error = center_of_image - center_of_line
angular.z = -Kp * error
linear.x = constant_speed
```

This ensures continuous correction toward the track center.

---

## 🔄 Failure Handling Logic

When the line is lost:

1. The robot uses the last known error
2. Amplifies correction (recovery behavior)
3. Reduces forward motion
4. Searches for the track again

Even without vision, it keeps trying to recover.

---

## 🏁 Mission Completion Logic

The robot:

1. Detects track markers
2. Tracks lap progress
3. Confirms completion condition
4. Executes safe shutdown sequence

It stops only when the mission is complete.

---

## ⚙️ Constraints

You are allowed to modify **ONLY TWO FILES**:

### 1️⃣ `custom_turtlebot3.sdf`

You may adjust:

- Camera position and angle
- Wheel friction and inertia
- Robot stability parameters
- Sensor configuration

**🎯 Goal:** Make the robot physically stable for vision control.

### 2️⃣ `follower_node.py`

You may improve:

- Vision processing pipeline
- Threshold tuning
- Control stability
- Recovery behavior
- Marker detection logic

**🎯 Goal:** Make the robot intelligent and robust.

---

## 🧪 Bonus Challenges

### 🔥 PID Control Upgrade

Replace proportional control with:

- **P** → correction
- **I** → drift correction
- **D** → smooth motion

### 📊 Live Dashboard

Display in real-time:

- Error value
- Angular velocity
- Linear velocity
- Distance traveled
- Lap progress

### 🏎 Adaptive Speed Control

- Slow down on sharp curves
- Speed up on straight paths
- Adjust speed dynamically based on error

### 🗺 Custom Track Challenge

Design your own Gazebo track:

- Curves
- Sharp turns
- Loops
- Marker zones

Then test: **Can your robot survive your own world?**

---

## 📦 Deliverables

### 🎥 1. Demonstration Video

Must include:

- Robot startup
- Line tracking
- Recovery behavior
- Full lap completion
- Safe shutdown

### 📁 2. GitHub Repository

Must contain:

- `/src` directory
- `custom_turtlebot3.sdf`
- `follower_node.py`
- Launch files
- README documentation

### 📄 3. Short Technical Report

Explain:

- System design approach
- Vision pipeline
- Control logic
- Challenges faced
- Tuning process

---

## 🏁 Final Message

This is not just a simulation project.

It is a complete robotics loop:

**See → Understand → Correct → Move → Fail → Recover → Improve**

If your robot completes this challenge successfully, then you haven't just written code —

**you have built a working autonomous system.**