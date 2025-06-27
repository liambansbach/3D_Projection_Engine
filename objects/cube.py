import numpy as np
import math_sm as math
import scene as scene
from vispy import scene as vispyscene
from .base import SceneObject

class Cube(SceneObject):
    def __init__(self, id: int = 0):
        super().__init__(id)
        self.points, self.primitives = self.create_cube()

    def create_cube(self):
        """
        Create an Cube at a given origin.
        """
        cube_points = np.array([
            [0, 0, 0],
            [0, 1, 0],
            [1, 1, 0],
            [1, 0, 0],
            [0, 0, 1],
            [0, 1, 1],
            [1, 1, 1],
            [1, 0, 1]
        ])

        cube_faces = np.array([
            [0,1,2,3],
            [4,5,6,7],
            [0,4,5,1],
            [2,3,7,6],
            [1,2,6,5],
            [0,3,7,4]
        ])

        return cube_points, cube_faces
    
    def init_vispy_visuals(self, viewbox):
        # 3 Achsenlinien
        for color in ['red', 'green', 'blue']:
            line = vispyscene.visuals.Line(pos=np.zeros((2, 3)), color=color, width=2, parent=viewbox.scene)
            self.axes.append(line)