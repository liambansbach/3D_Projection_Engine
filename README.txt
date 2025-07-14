3D_Projection_Engine
=====================

A minimal 3D scene engine that simulates a pinhole camera projection system in real-time using Python and Vispy. 
The engine allows interactive placement and control of 3D objects and cameras, and renders both 3D views and 2D projections.

---

Project Goal
------------

This project simulates a simple 3D world and its projection onto a 2D image plane, much like a game engine or graphics pipeline.

Key features:

- Construct scenes from 3D primitives (e.g. cubes)
- Add and control multiple cameras (position, orientation, intrinsic parameters)
- Visualize both the 3D scene and the projected 2D image coordinates
- Interact with the scene in real-time using keyboard input

---

Requirements
------------

- Python 3.x
- numpy
- vispy

Install dependencies with:

    pip install numpy vispy

---

Project Structure
-----------------

    3D_Projection_Engine/
    ├── main.py              # Entry point: window setup, event loop, rendering
    ├── scene.py             # Scene manager: stores and updates 3D objects and cameras
    ├── input_handler.py     # Keyboard input manager
    ├── scene_controller.py  # Handles per-frame updates (movement, rotation, object switching)
    ├── math_sm.py           # Linear algebra utilities (rotation, translation, pose matrix)
    ├── objects/
    │   ├── base.py          # Base class for all scene objects
    │   ├── cube.py          # Cube object with vertex and face definitions
    │   └── camera.py        # Camera object with intrinsic matrix and visualization
    └── README.md            # This document

---

Usage Guide
-----------

1. Running the Engine

    Start with:

        python main.py

    This launches a Vispy window displaying the 3D scene with a first camera and some cubes.

2. Controls

    - Move the selected object:
      - W/S: forward/back
      - A/D: left/right
      - Space/Ctrl: up/down
    - Rotate:
      - Q/E: yaw
      - Arrow keys: pitch/roll
    - Scale:
      - + / - : increase/decrease size
    - Reset: R resets position, rotation, and scale
    - Switch active object: 1
    - Create object: U adds a cube at a random position
    - Delete object: I
    - Add camera: K

---

Camera & Projection
-------------------

Each camera is defined by intrinsic parameters (f, o_x, o_y) and visualized with a frustum and axis lines. The projection follows the standard pinhole model:

    x = K · R · (X_w − T)

Cameras can be added dynamically and will appear in the 3D view. Intrinsics are set on creation.

---

Features
--------

- Object hierarchy (cubes, cameras) with shared transform logic
- Modular input and update handling
- Real-time FPS display
- Scalable rendering with Vispy
- Support for multiple cameras and object selection

---

Possible Extensions
-------------------

- Draw edges and faces for cube geometry
- Depth-based color shading
- Mouse-based object manipulation
- Support for additional primitives (spheres, planes, etc.)

---

Background
----------

This engine is built around the core concepts of 3D graphics and computer vision (Computer Vision II: Multiple View Geometry (3D Computer Vision) (IN2228)):

- Pinhole camera model
- Homogeneous transformations
- Real-time interaction
- Scene graphs and object hierarchies

It serves as a hands-on learning project and a foundation for more advanced visual computing applications (e.g. rendering, robotics, SLAM, AR).

---

Future Plans
------------

As the next step, the engine is intended to serve as a playground for implementing and visualizing classic computer vision algorithms covered in lecture. Planned additions include:

- 8-Point Algorithm
- Bundle Adjustment
- Simultaneous Localization and Mapping (SLAM)
- 3D Reconstruction from Multiple Views

These features are not implemented yet, but the architecture is being developed with these goals in mind.

---

Getting Started
---------------

Start modifying main.py. From there, you can explore the scene, camera, and controller modules.
