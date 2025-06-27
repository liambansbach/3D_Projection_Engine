📁 3D_Projection_Engine
│
├── camera.py           # Kameraklasse: Position, Rotation, Projektionsmatrix
├── scene.py            # Enthält Weltpunkte (z. B. Würfel)
├── projection.py       # Mathematische Transformationen: Welt → Kamera → Bild
├── main.py             # Hauptprogramm: Fenster, Rendering, Steuerung
└── README.txt          # Dieses Dokument

README.txt
===========

## 🎯 Projektziel

Dieses Projekt simuliert eine einfache **3D-Welt mit Projektion auf eine 2D-Bildebene**, wie in einer Game Engine.

Du baust:

- eine kleine Welt aus 3D-Punkten
- eine steuerbare Kamera mit Position und Blickrichtung
- eine 2D-Projektionsanzeige, die zeigt, **wo diese Punkte im Kamerabild erscheinen**

---

## ✅ Voraussetzungen

- Python 3.x
- `numpy`
- `pygame` (für Fenster und Anzeige)

Installieren mit:

```
pip install numpy pygame
```

---

## 📦 Struktur & Module

### camera.py

- Klasse `Camera`
  - Position `T` (Translation)
  - Rotation `R` ( Rotation als Matrix)
  - Methoden: `move(direction)`, `rotate(axis, angle)`
  - Methode: `get_view_matrix()` und `get_K()` (Kameramatrix)

### scene.py

- Definiert Weltpunkte, z. B. 3D-Würfel oder Gitter
- Rückgabe: Liste von `np.array`-Vektoren mit Koordinaten in Weltbezug

### projection.py

- Funktionen:
  - `world_to_camera(X_w, R, T)` → X_c
  - `project(X_c, K)` → 2D-Bildpunkt (u, v)
- Nutzt perspektivische Projektion nach dem Pinhole-Modell

### main.py

- Öffnet ein `pygame`-Fenster (z. B. 1920×1080)
- Lädt Szene
- Steuert Kamera mit Tasten
- Zeichnet projizierte Punkte

---

## 🧩 Schritt-für-Schritt Anleitung

### 1. Weltpunkte definieren (scene.py)

- z. B. Würfel mit 8 Ecken:
  ```python
  np.array([
      [0, 0, 0],
      [1, 0, 0],
      [1, 1, 0],
      [0, 1, 0],
      [0, 0, 1],
      [1, 0, 1],
      [1, 1, 1],
      [0, 1, 1],
  ])
  ```

### 2. Kamera erstellen (camera.py)

- Startposition: T = [0, 0, 5]
- Startrotation: R = Identity (np.eye(3))
- Steuerung per Tastatur (WASD, QE etc.)

### 3. Projektion implementieren (projection.py)

- Welt → Kamera:
  ```python
  X_c = R @ (X_w - T)
  ```
- Kamera → Bild:
  ```python
  x_hom = K @ X_c
  u = x_hom[0] / x_hom[2]
  v = x_hom[1] / x_hom[2]
  ```

### 4. Fenster & Rendering (main.py)

- Fenster mit pygame
- Punkte als Kreise auf 2D-Fläche zeichnen
- Clipping für Punkte außerhalb von (0, 1920), (0, 1080)

### 5. Interaktion

- Bewegung mit Tasten (WASDQE)
- Optional: Mausrotation
- Optional: UI-Overlay mit Position, FOV etc.

---

## ✨ Erweiterungsideen

- Linien zwischen Punkten (Würfelkanten)
- Farbcodierung nach Tiefe (z → Farbe)
- Dynamische Brennweite mit Mausrad
- Export als Screenshot oder GIF
- Zweite Kamera (z. B. Top-Down)

---

## 🧠 Hintergrundwissen

- Pinhole-Kameramodell:
  ```
  x = K · R · (X_w − T)
  ```
- Du simulierst, was Game Engines machen (Unreal, Unity, Blender)
- Alles basiert auf numpy + einfacher 2D-Darstellung

---

## 🏁 Starten

Beginne mit der Datei `main.py`. Von dort werden `scene`, `camera` und `projection` eingebunden.
