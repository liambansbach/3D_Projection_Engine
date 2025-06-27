import numpy as np
from scene import Scene
from objects.camera import Camera
from objects.base import SceneObject

def project_3d_to_2d(current_scene: Scene, current_camera: Camera):
    X_world = current_scene.get_all_points()
    R = current_camera.R
    T = current_camera.T
    f = current_camera.f
    o_x = current_camera.o_x
    o_y = current_camera.o_y

    X_camera = (R @ (X_world - T).T).T

    x_2d = []
    for X in X_camera:
        if X[2] != 0:
            u = f * (X[0] / X[2]) + o_x
            v = f * (X[1] / X[2]) + o_y
            x_2d.append([u, v])

    return np.array(x_2d, dtype=np.float32)


