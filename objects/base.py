import numpy as np
import math_sm as math
import scene as scene
from vispy import scene as vispyscene

# base_object (Parent Class)
class SceneObject:
    def __init__(self, 
                 #obj_type="generic", 
                 id: int = 0):
        self.id = id
        
        self.T = np.zeros(3)       #Position Vector
        self.R = np.eye(3)         #Rotation Matrix
        self.points:np.ndarray = np.empty((0, 3))  # Leeres (n, 3) Array
        self.primitives = []  # list of all Faces, Lines, Planes... (indizes of points that make up a line, face, plane... -> [[0,1], [3, 4, 5]]...)
        self.line_objects = [] # currently list of vispy objects  # vispy.Lines (für 2er-Listen)
        #self.line_object = None  # ein einziges Linienobjekt
        self.face_objects = [] # currently list of vispy objects  # vispy.Meshes (für 3+ Punkte)
        #self.axes = []
        self.scale = 1.0
        self.dirty:bool = True # Dirty Flag indicates if a object moved and if it needs to be redrawn.

    def __del__(self):
        print(f"{self.type} object with ID *{self.id}* deleted")

    @property
    def type(self):
        return self.__class__.__name__.lower()
    
    def get_T(self):
        return self.T
    
    def get_R(self):
        return self.R
    
    def get_type(self):
        return self.type

    def get_points(self):
        return self.points * self.scale # points are referenced on the local koordinate system of the object
    
    def get_transformed_points(self): # transformed points are transformed from local -> world coordinates!
        if len(self.points) == 0:
            return np.empty((0, 3), dtype=np.float32)
        
        #print("sooos: ", points)
        return (self.R @ np.array(self.points * self.scale).T).T + self.T
    
    def get_faces(self):
        return self.faces
    
    def get_pose(self): #Create the Pose Matrix in homogeneous coordinates (4x4)
        pose = np.zeros((4,4))
        pose[:3, :3]=self.R
        pose[:3, 3]=self.T
        pose[3,:]=np.array([0,0,0,1])
        return pose
    
    def rotate_object(self, axis: np.ndarray, angle: float):
        self.R = math.rotate(axis=axis, angle=angle, R=self.R) # Apply rotation in local frame
        self.dirty = True
        #self.update_object_location()

    def translate_object(self, u: np.ndarray):
        self.T = math.translate(u=u, T=self.T, R=self.R)
        self.dirty = True
        #self.update_object_location()

    def rescale_object(self, new_scale: float):
        self.scale = new_scale
        self.dirty = True

    def reset_object_position(self):
        self.R = np.eye(3)
        self.T = np.zeros(3)
        self.scale = 1.0
        self.dirty = True
        #self.update_object_location()

    def get_object_coordinate_system(self): #DEPRECATED
        c_1 = self.T + self.R[:,0]
        c_2 = self.T + self.R[:,1]
        c_3 = self.T + self.R[:,2]

        return c_1, c_2, c_3

    def get_local_bounding_box(self):
        # go through all points that make up an object and define a bounding box of that object based on its points in the local coordinate system
        max_x = 0
        max_y = 0
        max_z = 0
        min_x = 0
        min_z = 0
        min_y = 0
        points = self.get_points
        for point in points:
            if point[0]>max_x:
                max_x = point[0]
            #...
        pass