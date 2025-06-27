import numpy as np
from vispy import app, scene
#from objects.camera import Camera
from scene import Scene
from input_handler import InputHandler
from controller.scene_controller import update_scene
import time


# --------- Szene definieren (Würfelpunkte) ----------

input_handler = InputHandler()

world = Scene()
origin = world.origin
e_1, e_2, e_3 = world.get_world_axis()

cube1 = world.create_object(type="cube")
cube1.translate_object(u=np.array([0, 0, 10])) 

cube2 = world.create_object(type="cube")
cube2.translate_object(u=np.array([10, 0, 20])) 


window_size = [1080,720]

# --------- Kamera Setup ----------
camera_resolution = [1080, 720]
camera1 = world.create_camera(f=200, o_x=camera_resolution[0]/2, o_y=camera_resolution[1]/2) # 800x600 Bild

R = camera1.get_R()
T = camera1.get_T()
K = camera1.get_K()

# --------- 3D Szene (linkes Fenster) ----------

all_object_points = world.get_all_points()

canvas3d = scene.SceneCanvas(keys='interactive', title='3D Szene', size=(window_size[0], window_size[1]), show=True)
view3d = canvas3d.central_widget.add_view()
view3d.camera = scene.TurntableCamera(up='z', fov=45, distance=8)

scatter3d = scene.visuals.Markers()
scatter3d.set_data(all_object_points, edge_color='white', face_color='red', size=10)
view3d.add(scatter3d)

# Koordinatensystem der Welt und Achsen visualisieren
world.draw_world_axis_vispy(view3d)

# draw all cameras
world.draw_vispy_cameras(view3d)

# Event Listener

start_time = time.time()
current_fps:int = 0
recent_fps = []

def calc_fps(end_time):
    global start_time
    global current_fps
    global canvas3d
    elapsed_ms = (end_time - start_time) * 1000
    if elapsed_ms > 0:
        current_fps= int(1000 / elapsed_ms)
    else:
        current_fps= 000
    
    if len(recent_fps) >= 100:
        recent_fps.pop(-1)
    recent_fps.append(current_fps)
    #print(len(recent_fps))
    display_fps:int = int(sum(recent_fps)/len(recent_fps))

    start_time = end_time
    canvas3d.title = f"3D Szene: {display_fps} FPS"
    

@canvas3d.events.key_press.connect
def on_key_press(event):
    key = event.key.name
    input_handler.key_press(key)

@canvas3d.events.key_release.connect
def on_key_release(event):
    key = event.key.name
    input_handler.key_release(key)

def tick(event):
    update_scene(input_handler, world, scatter3d, view3d)
    current_time = time.time()
    calc_fps(end_time=current_time)
    

timer = app.Timer(interval=1/60, connect=tick, start=True)

app.run()






# def project_points(X_w, R, T, K):
#     X_c = (R @ (X_w - T).T).T
#     x_hom = (K @ X_c.T).T
#     uv = x_hom[:, :2] / x_hom[:, 2, np.newaxis]
#     return uv



# # --------- 2D Projektion (rechtes Fenster) ----------
# canvas2d = scene.SceneCanvas(title='2D Projektion', size=(800, 600), show=True)
# view2d = canvas2d.central_widget.add_view()
# view2d.camera = scene.PanZoomCamera(rect=(0, 0, 800, 600))
# view2d.camera.aspect = 1
# view2d.camera.flip = (False, True)  # y-Achse umdrehen

# scatter2d = scene.visuals.Markers()
# view2d.add(scatter2d)

# # --------- Update Funktion für 2D-Projektion ----------
# def update_projection(event=None):
#     uv = project_points(cube_points, camera1.get_R(), camera1.get_T(), camera1.K)
#     scatter2d.set_data(uv, edge_color='black', face_color='blue', size=8)

# --------- Timer für Live-Update ----------
#timer = app.Timer(interval=0.05, connect=update_projection, start=True)


