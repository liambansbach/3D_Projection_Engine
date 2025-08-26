import numpy as np
from scene import Scene
from objects.camera import Camera
from objects.base import SceneObject
import math_sm as math_sm

"""
All Versions of the Function "project_3d_to_2d" return the same output but differ in performance!
"""

# def project_3d_to_2d(current_scene: Scene, current_camera: Camera):
#     X_world = current_scene.get_all_points()
#     R = current_camera.R
#     T = current_camera.T
#     f = current_camera.f
#     o_x = current_camera.o_x
#     o_y = current_camera.o_y

#     # world → camera coordinates
#     X_camera = (R.T @ (X_world - T).T).T

#     x_2d = []
#     for X in X_camera:
#         if X[2] <= 0:
#             continue  # ignore points behind the camera
#         u = f * (X[0] / X[2]) + o_x
#         v = f * (X[1] / X[2]) + o_y
#         x_2d.append([u, v])
#     return np.array(x_2d, dtype=np.float32)

# def project_3d_to_2d(current_scene: Scene, current_camera: Camera):
#     # lambda * x = K * PI_0 * g * X
#     """
#     Project all the 3D Points of a scene to the currently active camera image plane.

#     Return np.array(N, [u, v])
#     -> N 2d points.
#     """
#     X_world = current_scene.get_all_points()
#     K = current_camera.get_K()
#     PI_0 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
#     R = current_camera.get_R()
#     T = current_camera.get_T()
#     g_cw = math_sm.make_homogeneous(R=R, T=T)  # Camera → World
#     g_wc = np.linalg.inv(g_cw)                  # World → Camera

#     x_2d =[]

#     PI = K @ PI_0 @ g_wc

#     for X in X_world:
#         X_h = np.ones(4)
#         X_h[:3] = X
#         x = PI @ X_h

#         depth = x[-1]

#         if depth > 0:
#             x_norm = x / depth
#             x_2d.append([x_norm[0], x_norm[1]])

#     #print(x_2d)
    

#     return np.array(x_2d, dtype=np.float32)


def project_3d_to_2d(current_scene: Scene, current_camera: Camera):
    """
    Project all the 3D Points of a scene to the currently active camera image plane.

    Return np.array(N, [u, v])
    -> N 2d points.
    """
    X = current_scene.get_all_points()                # (N,3), float32 ideal
    K = current_camera.get_K()                           # (3,3)
    R = current_camera.get_R()                           # (3,3)
    T = current_camera.get_T().reshape(3, 1)             # (3,1) Camera Position in World coordinates

    # World -> Camera without using inverse:
    # X_c = R^T (X_w - T)
    Xc = (R.T @ (X.T - T)).T                  # (N,3)

    # Filter points laying behind the camera
    z = Xc[:, 2]
    mask = z > 0
    if not np.any(mask):
        return np.empty((0, 2), dtype=np.float32)

    Xc = Xc[mask]                             # (M,3)

    # Project all points in one go
    xh = (K @ Xc.T).T                         # (M,3) = homogen in Pixel
    uvs = xh[:, :2] / xh[:, 2:3]              # (M,2)

    return uvs.astype(np.float32)
