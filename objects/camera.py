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
