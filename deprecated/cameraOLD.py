import numpy as np
import math_sm as math
from vispy import scene


class CameraOLD:
    def __init__(self, f:float, o_x:float, o_y:float, s_x:float=1, s_y:float=1, s_theta:float=0):
        self.T = np.zeros(3)       #Position Vector
        self.R = np.eye(3)         #Rotation Matrix
        self.f = f                 #Focal length in mm
        self.o_x = o_x             #Image center in Pixeln (Principal Point)
        self.o_y = o_y             #Image center in Pixeln (Principal Point)
        self.s_x = s_x             #Scaling pixelrange in x dimension (How many cm correspond to one pixel)
        self.s_y = s_y             #Scaling pixelrange in y dimension (How many cm correspond to one pixel)
        self.s_theta = s_theta     #Skew factor (Curvature of lense)
        self.K = np.array(         #Create Camera matrix
            [
                [f * s_x, f * s_theta, o_x],
                [0, f * s_y, o_y],
                [0,0,1]
            ])
        self.visuals = {'lines': [], 'axes': []}  # getrennte Listen
        self.fov = 70
        self.aspect = 1.0
        self.scale = 2.0
        self.id:int = 0

    def __del__(self):
        print("camera deleted")
        
    def get_T(self):
        return self.T
    
    def get_R(self):
        return self.R
    
    def get_K(self):
        return self.K
    
    def get_pose(self): #Create the Pose Matrix in homogeneous coordinates (4x4)
        pose = np.zeros((4,4))
        pose[:3, :3]=self.R
        pose[:3, 3]=self.T
        pose[3,:]=np.array([0,0,0,1])
        return pose
    
    def rotate_camera(self, axis: np.ndarray, angle: float):
        self.R = math.rotate(axis=axis, angle=angle, R=self.R) # Apply rotation in local frame

    def translate_camera(self, u: np.ndarray):
        self.T = math.translate(u=u, T=self.T, R=self.R)

    def get_camera_coordinate_system(self): #DEPRECATED
        c_1 = self.T + self.R[:,0]
        c_2 = self.T + self.R[:,1]
        c_3 = self.T + self.R[:,2]

        return c_1, c_2, c_3
    
    def reset_camera_position(self):
        self.R = np.eye(3)
        self.T = np.zeros(3)
        self.scale = 2
    
    # def init_visuals(self, viewbox, fov=70, aspect=1.0, scale=2.0):
    #     self.fov = fov
    #     self.aspect = aspect
    #     self.scale = scale

    #     self.visuals = {'lines': [], 'axes': []}

    #     # 4 Sichtlinien + 4 Umrandung + 12 Quaderkanten = 20 Linien
    #     for _ in range(20):
    #         line = scene.visuals.Line(pos=np.zeros((2, 3)), color='orange', width=1, parent=viewbox.scene)
    #         self.visuals['lines'].append(line)

    #     # 3 Achsenlinien
    #     for color in ['red', 'green', 'blue']:
    #         line = scene.visuals.Line(pos=np.zeros((2, 3)), color=color, width=2, parent=viewbox.scene)
    #         self.visuals['axes'].append(line)

    #     self.update_visuals()

    # def update_visuals(self):
    #     R = self.R
    #     T = self.T.reshape(3)
    #     fov = self.fov
    #     aspect = self.aspect
    #     scale = self.scale

    #     # === Sichtfeld ===
    #     z = scale * 0.6
    #     h = np.tan(np.radians(fov / 2)) * z
    #     w = h * aspect
    #     image_plane = np.array([
    #         [-w, -h, z],
    #         [ w, -h, z],
    #         [ w,  h, z],
    #         [-w,  h, z],
    #     ])
    #     image_plane_world = (R @ image_plane.T).T + T

    #     for i in range(4):  # Sichtlinien zur Bildebene
    #         self.visuals['lines'][i].set_data(pos=np.array([T, image_plane_world[i]]))

    #     for i in range(4):  # Rechteckrahmen
    #         p1 = image_plane_world[i]
    #         p2 = image_plane_world[(i+1)%4]
    #         self.visuals['lines'][4 + i].set_data(pos=np.array([p1, p2]))

    #     # === Gehäuse (Quader) ===
    #     box_depth = scale * 1.2
    #     box_size = scale * 0.3
    #     local_box = np.array([
    #         [-box_size, -box_size, 0],
    #         [ box_size, -box_size, 0],
    #         [ box_size,  box_size, 0],
    #         [-box_size,  box_size, 0],
    #         [-box_size, -box_size, -box_depth],
    #         [ box_size, -box_size, -box_depth],
    #         [ box_size,  box_size, -box_depth],
    #         [-box_size,  box_size, -box_depth],
    #     ])
    #     box_world = (R @ local_box.T).T + T
    #     edges = [(0,1),(1,2),(2,3),(3,0), (4,5),(5,6),(6,7),(7,4), (0,4),(1,5),(2,6),(3,7)]

    #     for i, (i1, i2) in enumerate(edges):
    #         self.visuals['lines'][8 + i].set_data(pos=np.array([box_world[i1], box_world[i2]]))

    #     # === Achsen ===
    #     axis_length = scale * 0.5
    #     axes = [
    #         (np.array([0, 0, 0]), np.array([axis_length, 0, 0])),
    #         (np.array([0, 0, 0]), np.array([0, axis_length, 0])),
    #         (np.array([0, 0, 0]), np.array([0, 0, axis_length])),
    #     ]
    #     for i, (start, end) in enumerate(axes):
    #         start_world = (R @ start) + T
    #         end_world = (R @ end) + T
    #         self.visuals['axes'][i].set_data(pos=np.array([start_world, end_world]))

    def get_visual_geometry(self):
        """
        Gibt die 3D-Positionen der Sichtstrahlen und das Gehäuse zurück.
        Nur zur Weitergabe an die Visualisierung.
        """
        R = self.R
        T = self.T
        scale = self.scale
        fov = self.fov
        aspect = self.aspect

        z = scale * 0.6
        h = np.tan(np.radians(fov / 2)) * z
        w = h * aspect

        # Sichtstrahlen zur Bildfläche (4 Punkte)
        image_plane = np.array([
            [-w, -h, z],
            [ w, -h, z],
            [ w,  h, z],
            [-w,  h, z],
        ])
        image_plane_world = (R @ image_plane.T).T + T

        # Kamera-Gehäuse (8 Punkte, Quader)
        box_depth = scale * 1.2
        box_size = scale * 0.3
        local_box = np.array([
            [-box_size, -box_size, 0],
            [ box_size, -box_size, 0],
            [ box_size,  box_size, 0],
            [-box_size,  box_size, 0],
            [-box_size, -box_size, -box_depth],
            [ box_size, -box_size, -box_depth],
            [ box_size,  box_size, -box_depth],
            [-box_size,  box_size, -box_depth],
        ])
        box_world = (R @ local_box.T).T + T

        return {
            "origin": T,
            "image_plane": image_plane_world,
            "box": box_world
        }
