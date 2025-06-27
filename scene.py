import numpy as np
#from camera import Camera
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
        #self.objects = []  # Liste aller Objekte (Cubes)
        self.pressed_keys = set()  # Tastatur-Event-Handler
        self.objects_list: list[SceneObject] = []
        #self.camera_list: list[Camera] = []
        #self.current_camera: Camera = None
        self.current_object: SceneObject = None
        self.camera_lines = None


    def get_world_axis(self):
        return self.e_1, self.e_2, self.e_3
    
    def create_camera(self, f:float, o_x:float, o_y:float, s_x:float=1, s_y:float=1, s_theta:float=0):
        object_id = len(self.objects_list)
        camera = Camera(f=f, o_x=o_x, o_y=o_y, s_x=s_x, s_y=s_y, s_theta=s_theta, id=object_id)
        #self.camera_list.append(camera)
        #self.current_camera = camera
        
        self.current_object = camera
        self.objects_list.append(camera)

        print("added Camera ID: ", camera.id)

        return camera
    
    def delete_camera(self, id: int):
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
        all_cameras: list[Camera] = []

        for obj in self.objects_list:
            if isinstance(obj, Camera):
                all_cameras.append(obj)

        return all_cameras

    # Kameras visualisieren mit Vispy
    def draw_vispy_cameras(self, viewbox):
        self.camera_lines = scene.visuals.Line(
            pos=np.zeros((0, 3)),  # leerer Start
            color=np.zeros((0, 4)),
            width=2,
            connect='segments',
            method='gl',
            parent=viewbox.scene
        )

    
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

    def get_all_points(self):
        """
        Gibt alle Punkte der Szene zurück (flach zusammengeführt) BIS AUF KAMERA PUNKTE
        """
        if not self.objects_list:
            return np.empty((0, 3), dtype=np.float32)

        all_points = []
        for obj in self.objects_list:
            if isinstance(obj, Camera) == False:
                all_points.append(obj.get_transformed_points())  # shape (m, 3)

        points = np.vstack(all_points).astype(np.float32)  # shape (N, 3)
        #print("points: ", points)
        return points
    
    def get_object_points(self, object: SceneObject):
        """
        Gibt alle Punkte eines Objekts zurück (flach zusammengeführt)
        """
        all_points = object.get_points()

        points = np.vstack(all_points).astype(np.float32)
        return points
    
    def draw_world_axis_vispy(self, viewbox):
        """
        Zeichnet die Kamera als Quader + Sichtfeldpyramide + Koordinatensystem
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


    def get_all_camera_line_segments(self):
        """
        Gibt alle Kameralinien als segmentweise Positionen und Farben zurück.
        Die aktive Kamera wird hervorgehoben (orange), andere grau.
        """
        all_segments = []
        all_colors = []

        for obj in self.objects_list:
            if not isinstance(obj, Camera):
                continue

            is_active = (obj == self.current_object)

            R = obj.R
            T = obj.T
            scale = obj.scale * 2
            points = obj.points * obj.scale
            edges = obj.primitives

            points_world = (R @ points.T).T + T

            for edge in edges:
                p1 = points_world[edge[0]]
                p2 = points_world[edge[1]]
                all_segments.extend([p1, p2])

                color = [1.0, 0.5, 0.0, 1.0] if is_active else [0.5, 0.5, 0.5, 1.0]  # orange vs grau
                all_colors.extend([color, color])

        if not all_segments:
            return np.zeros((0, 3), dtype=np.float32), np.zeros((0, 4), dtype=np.float32)

        return (
            np.array(all_segments, dtype=np.float32),
            np.array(all_colors, dtype=np.float32)
        )

