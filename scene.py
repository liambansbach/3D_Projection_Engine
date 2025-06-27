import numpy as np
import math_sm as math
from vispy import scene
from objects.camera import Camera
from objects.cube import Cube
from objects.base import SceneObject

class Scene:
    def __init__(self,origin: np.ndarray=np.array([0,0,0]), e_1: np.ndarray=np.array([1,0,0]), e_2: np.ndarray=np.array([0,1,0]), e_3: np.ndarray=np.array([0,0,1])):
        self.origin = origin
        self.e_1 = e_1 # e_1 (x-Axis) of the World
        self.e_2 = e_2 # e_2 (y-Axis) of the World
        self.e_3 = e_3 # e_3 (z-Axis) of the World
        self.pressed_keys = set()  # Tastatur-Event-Handler
        self.objects_list: list[SceneObject] = []
        self.current_object: SceneObject = None
        self.camera_lines = None

    def get_world_axis(self):
        return self.e_1, self.e_2, self.e_3
        
    def get_all_points(self):
        """
        Return a List of all Points that are Part of the current scene (Ignoring Camera Points)
        """

        if not self.objects_list:
            return np.empty((0, 3), dtype=np.float32)

        all_points = []
        for obj in self.objects_list:
            if isinstance(obj, Camera) == False:
                all_points.append(obj.get_transformed_points())  # shape (m, 3)

        points = np.vstack(all_points).astype(np.float32)  # shape (N, 3)
        return points
    
    def draw_world_axis_vispy(self, viewbox):
        """
        Draw the World Coordinatesystem and a fine Kertesian Grid into the world
        """
        # Linien definieren: jeweils vom Ursprung zur Achsenspitze
        axis_lines = [
            (self.origin, self.e_1),
            (self.origin, self.e_2),
            (self.origin, self.e_3),
        ]

        colors = ['red', 'green', 'blue']  # x, y, z

        for (start, end), color in zip(axis_lines, colors):
            line = scene.visuals.Line(
                pos=np.array([start, end]),
                color=color,
                width=3,
                parent=viewbox.scene
            )

        for (start, end), color in zip(axis_lines, ['grey', 'grey', 'grey']):
            line = scene.visuals.Line(
                pos=np.array([start, end*50]),
                color=color,
                width=1,
                parent=viewbox.scene
            )

# region Object Methods

    def create_object(self, type: str):
        object_id = len(self.objects_list)
        if type=="cube":
            my_object = Cube(id=object_id)
            self.objects_list.append(my_object)

        print(f"{type} object with ID *{my_object.id}* created.")
        self.current_object = my_object

        return my_object
    
    def delete_object(self):
        # Iteriere rückwärts über die Objekte
        for obj in reversed(self.objects_list):
            object_type = obj.type
            if isinstance(obj, Camera) == False:
                self.objects_list.remove(obj)
                self.current_object = self.objects_list[-1]
                #print(f"{object_type} object with ID *{obj.id}* deleted.")
                del obj
                break  # nur das erste passende Objekt löschen

    def get_object_points(self, object: SceneObject):
        """
        Gibt alle Punkte eines Objekts zurück (flach zusammengeführt)
        """
        
        all_points = object.get_points()

        points = np.vstack(all_points).astype(np.float32)
        return points

# endregion

# region Camera Methods

    def create_camera(self, f:float, o_x:float, o_y:float, s_x:float=1, s_y:float=1, s_theta:float=0):
        """
        Create a Cameraobject given its Parameters
        """

        object_id = len(self.objects_list)
        camera = Camera(f=f, o_x=o_x, o_y=o_y, s_x=s_x, s_y=s_y, s_theta=s_theta, id=object_id)
        
        self.current_object = camera
        self.objects_list.append(camera)

        print("added Camera ID: ", camera.id)
        return camera
    
    def delete_camera(self, id: int):
        """
        Delete a Cameraobject, given an ID
        """

        for obj in self.objects_list:
            type = obj.type()
            if isinstance(obj, Camera) and obj.id == id:
                self.objects_list.remove(obj)
                self.current_object = self.objects_list[-1]
                del obj
                break
            
            else:
                print(f"camera object with ID *{id}* does not exist!")
    
    def get_all_cameras(self):
        """
        Return all Camera objects in a List
        """

        all_cameras: list[Camera] = []
        for obj in self.objects_list:
            if isinstance(obj, Camera):
                all_cameras.append(obj)

        return all_cameras

    def init_vispy_objects(self, viewbox):
        """
        initialize the self.camera_lines and self.object_meshs Variable (initially NONE) as
        empty Vispy Objects
        """

        self.camera_lines = scene.visuals.Line(
            pos=None,  # leerer Start
            color=None,
            width=2,
            connect='segments',
            method='gl',
            parent=viewbox.scene
        )

    def get_all_camera_line_segments(self):
        """
        Return all Lines that make up Cameras as Segmentwise Positions and colors.
        The active Camera is highlighted in Orange, others in grey.
        """

        all_segments = []
        all_colors = []

        for obj in self.objects_list:
            if not isinstance(obj, Camera):
                continue

            # Add lines of the Rig
            is_active = (obj == self.current_object)
            R = obj.R
            T = obj.T
            points = obj.points * obj.scale
            edges = obj.primitives
            points_world = (R @ points.T).T + T
            for edge in edges:
                p1 = points_world[edge[0]]
                p2 = points_world[edge[1]]
                all_segments.extend([p1, p2])

                color = [1.0, 0.5, 0.0, 1.0] if is_active else [0.5, 0.5, 0.5, 1.0]  # orange vs grau
                all_colors.extend([color, color])

            # Add lines of the coordinate System in red, green, blue
            axis_length = obj.scale * 0.5
            axes = [
                (np.array([0, 0, 0]), np.array([axis_length, 0, 0])),   # x
                (np.array([0, 0, 0]), np.array([0, axis_length, 0])),   # y
                (np.array([0, 0, 0]), np.array([0, 0, axis_length])),   # z
            ]
            for i, (start, end) in enumerate(axes):
                p1 = (R @ start) + T
                p2 = (R @ end) + T
                all_segments.extend([p1, p2])

            for color in [[1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0], [0.0, 0.0, 1.0, 1.0]]: #red, green, blue
                all_colors.extend([color, color])


        if not all_segments:
            return np.zeros((0, 3), dtype=np.float32), np.zeros((0, 4), dtype=np.float32)

        return (
            np.array(all_segments, dtype=np.float32),
            np.array(all_colors, dtype=np.float32)
        )

# endregion