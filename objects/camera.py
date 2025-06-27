import numpy as np
import math_sm as math
import scene as scene
from vispy import scene as vispyscene
from .base import SceneObject

class Camera(SceneObject):
    def __init__(self, f:float, o_x:float, o_y:float, s_x:float=1, s_y:float=1, s_theta:float=0, id:int = 0):
        super().__init__(id)
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
        self.fov = 70
        self.aspect = 1.0
        self.points, self.primitives = self.build_camera_points()


    def build_camera_points(self): # init all the points that make up the camera rig (body)
        points = np.zeros((5,3))
        for i in range(points.shape[0]):
            match i:
                #case 0:
                    #do nothing
                case 1: # Punkt 1
                    points[i] = np.array([-self.o_x, self.o_y, self.f])
                case 2:
                    points[i] = np.array([self.o_x, self.o_y, self.f])
                case 3:
                    points[i] = np.array([self.o_x, -self.o_y, self.f])
                case 4:
                    points[i] = np.array([-self.o_x, -self.o_y, self.f])

        edges = np.array([
            [0, 1],
            [0, 2],
            [0, 3],
            [0, 4],
            [1, 2],
            [2, 3],
            [3, 4],
            [4, 1]
        ])

        points = points * self.scale * 0.001 # convert mm to m
        
        return points, edges

    
    def get_K(self):
        return self.K

    # def init_simple_visuals(self, viewbox):
    #     for edge in self.primitives:
    #         line = vispyscene.visuals.Line(pos=np.zeros((2, 3)), color='orange', width=1, parent=viewbox.scene)
    #         self.line_objects.append(line)

    #     # 3 Achsenlinien
    #     for color in ['red', 'green', 'blue']:
    #         line = vispyscene.visuals.Line(pos=np.zeros((2, 3)), color=color, width=2, parent=viewbox.scene)
    #         self.axes.append(line)

    # def update_simple_visuals(self):
    #     R = self.R
    #     T = self.T.reshape(3)
    #     scale = self.scale * 2
    #     points = self.points * self.scale
    #     edges = self.primitives

    #     points_world = (R @ points.T).T + T

    #     for i in range(edges.shape[0]):
    #         p1 = points_world[edges[i][0]]
    #         p2 = points_world[edges[i][1]]
    #         self.line_objects[i].set_data(pos=np.array([p1,p2]))
            

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
    #         self.axes[i].set_data(pos=np.array([start_world, end_world]))

    def init_simple_visuals(self, viewbox):
            # === Sichtfeld (ein Linienobjekt für Kamera-Rig) ===
        rig_lines = vispyscene.visuals.Line(
            pos=np.zeros((2, 3)),  # Platzhalter
            color='orange',
            width=2,
            connect='segments',
            method='gl',
            parent=viewbox.scene
        )
        self.line_objects.append(rig_lines)

        # === Achsenlinien (drei farbige Linien separat) ===
        for color in ['red', 'green', 'blue']:
            axis_line = vispyscene.visuals.Line(
                pos=np.zeros((2, 3)),
                color=color,
                width=2,
                parent=viewbox.scene
            )
            self.line_objects.append(axis_line)

    def update_simple_visuals(self):
        R = self.R
        T = self.T.reshape(3)
        scale = self.scale * 2
        points = self.points * self.scale
        edges = self.primitives

        points_world = (R @ points.T).T + T

        # === Sichtfeldlinien berechnen ===
        line_segments = []
        for edge in edges:
            p1 = points_world[edge[0]]
            p2 = points_world[edge[1]]
            line_segments.append(p1)
            line_segments.append(p2)

        all_segments = np.array(line_segments, dtype=np.float32)
        
        # === Sichtfeld (Index 0 in line_objects) ===
        self.line_objects[0].set_data(pos=all_segments)

        # === Achsen (Index 1–3 in line_objects) ===
        axis_length = scale * 0.5
        axes = [
            (np.array([0, 0, 0]), np.array([axis_length, 0, 0])),   # x
            (np.array([0, 0, 0]), np.array([0, axis_length, 0])),   # y
            (np.array([0, 0, 0]), np.array([0, 0, axis_length])),   # z
        ]
        for i, (start, end) in enumerate(axes):
            start_world = (R @ start) + T
            end_world = (R @ end) + T
            self.line_objects[i + 1].set_data(pos=np.array([start_world, end_world]))







    # def init_vispy_visuals(self, viewbox):
    #     # 4 Sichtlinien + 4 Umrandung + 12 Quaderkanten = 20 Linien
    #     for _ in range(20):
    #         line = vispyscene.visuals.Line(pos=np.zeros((2, 3)), color='orange', width=1, parent=viewbox.scene)
    #         self.line_objects.append(line)

    #     # 3 Achsenlinien
    #     for color in ['red', 'green', 'blue']:
    #         line = vispyscene.visuals.Line(pos=np.zeros((2, 3)), color=color, width=2, parent=viewbox.scene)
    #         self.axes.append(line)

    # def update_vispy_visuals(self):
    #     R = self.R
    #     T = self.T.reshape(3)
    #     fov = self.fov
    #     aspect = self.aspect
    #     scale = self.scale * 2

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
    #         self.line_objects[i].set_data(pos=np.array([T, image_plane_world[i]]))

    #     for i in range(4):  # Rechteckrahmen
    #         p1 = image_plane_world[i]
    #         p2 = image_plane_world[(i+1)%4]
    #         self.line_objects[4 + i].set_data(pos=np.array([p1, p2]))

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
    #         self.line_objects[8 + i].set_data(pos=np.array([box_world[i1], box_world[i2]]))

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
    #         self.axes[i].set_data(pos=np.array([start_world, end_world]))