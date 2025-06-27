import numpy as np
from scene import Scene
from objects.camera import Camera
from objects.cube import Cube
from objects.base import SceneObject
from input_handler import InputHandler
from vispy import scene as sc


def update_scene(input_handler: InputHandler, scene: Scene, scatter3d, view3d):

    #cam:Camera = scene.current_camera
    obj:SceneObject = scene.current_object
    

    # === Einmalige Aktionen ===
    if input_handler.was_pressed_once('U'):
        rand = np.random.normal(0, 1, 3) * 10
        new_object = scene.create_object(type="cube")
        new_object.translate_object(u=rand)
        scatter3d.set_data(scene.get_all_points(), edge_color='white', face_color='red', size=10)

    if input_handler.was_pressed_once('I') and len(scene.objects_list) > 1:
        scene.delete_object()
        scatter3d.set_data(scene.get_all_points(), edge_color='white', face_color='red', size=10)

    if input_handler.was_pressed_once('K'):
        camera_resolution = [1080, 720]
        new_camera = scene.create_camera(f=200, o_x=camera_resolution[0]/2, o_y=camera_resolution[1]/2) # 800x600 Bild
        # new_camera.init_vispy_visuals(view3d)
        # new_camera.update_vispy_visuals()

        # new_camera.init_simple_visuals(view3d)
        # new_camera.update_simple_visuals()
        
        #scene.draw_vispy_cameras(view3d)
        #scatter3d.set_data(scene.get_all_points(), edge_color='white', face_color='red', size=10)

    if input_handler.was_pressed_once('1'):
        
        if not scene.objects_list:
            print("Keine Objekte vorhanden.")
            return

        if scene.current_object is None:
            scene.current_object = scene.objects_list[0]
        else:
            current_index = scene.objects_list.index(scene.current_object)
            next_index = (current_index + 1) % len(scene.objects_list)
            scene.current_object = scene.objects_list[next_index]

        #print(f"Aktives Objekt: ID {scene.current_object.id}")
        print(f"Aktives Objekt: *{scene.current_object.type} object* with ID *{scene.current_object.id}*")
        

    # === Kontinuierliche Kamera-Steuerung ===
    speed = 0.1
    rot_speed = 1
    e1, e2, e3 = scene.get_world_axis()

    if input_handler.is_held('W'):
        #print("W pressed")
        obj.translate_object(np.array([0, 0, speed]))

    if input_handler.is_held('S'):
        obj.translate_object(np.array([0, 0, -speed]))

    if input_handler.is_held('A'):
        obj.translate_object(np.array([-speed, 0, 0]))

    if input_handler.is_held('D'):
        obj.translate_object(np.array([speed, 0, 0]))

    if input_handler.is_held('Space'):
        obj.translate_object(np.array([0, speed, 0]))

    if input_handler.is_held('Control'):
        obj.translate_object(np.array([0, -speed, 0]))


    if input_handler.is_held('Q'):
        obj.rotate_object(axis=obj.R @ e3, angle=-rot_speed)

    if input_handler.is_held('E'):
        obj.rotate_object(axis=obj.R @ e3, angle=rot_speed)

    if input_handler.is_held('Left'):
        obj.rotate_object(axis=obj.R @ e2, angle=-rot_speed)

    if input_handler.is_held('Right'):
        obj.rotate_object(axis=obj.R @ e2, angle=rot_speed)

    if input_handler.is_held('Up'):
        obj.rotate_object(axis=obj.R @ e1, angle=rot_speed)

    if input_handler.is_held('Down'):
        obj.rotate_object(axis=obj.R @ e1, angle=-rot_speed)


    if input_handler.is_held('R'):
        obj.reset_object_position()


    if input_handler.is_held('+'):
        obj.rescale_object(new_scale=obj.scale + 0.1)

    if input_handler.is_held('-') and obj.scale - 0.1 >= 0.5:
        obj.rescale_object(new_scale=obj.scale - 0.1)
 

    # if moved:
    #     if isinstance(obj, Camera):
    #         #obj.update_vispy_visuals()
    #         obj.update_simple_visuals()

    # if obj.dirty:
    #     if isinstance(obj, Camera):
    #         obj.update_simple_visuals()
    #         obj.dirty = False
    
    # elif isinstance(obj, Cube):
    #     if obj.dirty:
    #         #points = obj.get_transformed_points()
    #         scatter3d.set_data(scene.get_all_points(), edge_color='white', face_color='red', size=10)
    #         obj.dirty = False
                
    # DrawCall for camera objects
    segments, colors = scene.get_all_camera_line_segments()
    scene.camera_lines.set_data(pos=segments, color=colors)

    # DrawCall for Points
    scatter3d.set_data(scene.get_all_points(), edge_color='white', face_color='red', size=10)

    

    input_handler.end_frame()
