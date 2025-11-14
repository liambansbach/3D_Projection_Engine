import cv2 as cv
import numpy as np

def main():
    cap = cv.VideoCapture(0)

    cam_width = 640
    cam_height = 480
    cam_num_channels = 3
    t = 0 # zum zeichnen der sinuskurve

    cam_fps = 30
    delay_ms = int(1000/cam_fps)   


    if not cap.isOpened():
        print("Kamera konnte nicht geöffnet werden")
        exit()

    while True:
        ret, frame = cap.read()
        cam_height, cam_width, cam_num_channels = frame.shape

        gray_frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

        #anpassen von t für die sinus kurve
        t += delay_ms / 1000 
        if t >= np.pi * 2 : t = 0 # Wenn t größer als 2*pi, dann wieder auf 0 setzen, damit kein overflow passiert


        if not ret:
            print("Kein Frame erhalten (ret=False)")
            break

        #frame = draw_circle(frame=frame, center=(int(cam_width/2), int((cam_height/2)+np.sin(2*t)*100)), radius=20)
        frame = detect_faces(frame, gray_frame)
        cv.imshow("camera_image", frame)

        # WICHTIG: waitKey aufrufen, sonst friert das Fenster ein
        # Hier: mit 'q' beenden
        if cv.waitKey(delay_ms) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


def draw_circle(frame, center, radius, thickness=2):
    cv.circle(img=frame, center=center, radius=radius, color=(0, 0, 255), thickness=thickness)
    return frame

def detect_faces(frame, gray_frame):
    face_classifier = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
    face = face_classifier.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=10, minSize=(100, 100))
    for (x, y, w, h) in face:
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 4)

    return frame


if __name__ == "__main__":
    main()
