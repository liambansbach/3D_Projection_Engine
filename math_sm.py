import numpy as np

def vec_to_skew(u: np.ndarray):
    #assert u.shape == (3,), "shape of vector must be 3x1"
    if not isinstance(u, np.ndarray):
        raise TypeError("Input must be a numpy array")
    if u.shape != (3,):
        raise ValueError("Shape of input vector must be (3,)")
    
    skew = np.array([
        [0, -u[2], u[1]],
        [u[2], 0, -u[0]], 
        [-u[1], u[0], 0]
    ])
    return skew
    
def make_homogeneous(R: np.ndarray, T: np.ndarray): #Create the Pose Matrix in homogeneous coordinates (4x4)
    assert T.shape == (3,), "shape of vector must be 3x1"
    assert R.shape == (3,3), "shape of Matrix must be 3x3"

    pose = np.zeros((4,4))
    pose[:3, :3]=R
    pose[:3, 3]=T
    pose[3,:]=np.array([0,0,0,1])
    return pose


def rotate(axis: np.ndarray, angle: float, R: np.ndarray): # Rodriques Formula
        assert axis.shape == (3,), "Axis must be a 3D vector"

        angle = np.deg2rad(angle)  # Convert degrees to radians

        w = axis / np.linalg.norm(axis)  # Ensure it's a unit vector
        W_hat = vec_to_skew(w)      # Skew-symmetric matrix

        R_delta = (np.eye(3) + np.sin(angle) * W_hat + (1 - np.cos(angle)) * (W_hat @ W_hat))

        new_R = R_delta @ R  # Apply rotation in local frame

        return new_R


def translate(u: np.ndarray, T: np.ndarray, R: np.ndarray):
        """
        Verschiebt das Objekt in Weltkoordinaten.
        Der Vektor 'u' m wird dafür mit "R" in das Weltkoordinatensystem gedreht.

        Args:
            u (np.ndarray): 3D-Translationsvektor im lokalen Koordinatensystem.
        """
        assert u.shape == (3,), "u must be a 3D vector"
        new_T = R @ u +T  # u ist eine Verschiebung im lokalen Koordinatensystem der Kamera → wird zu Weltkoordinaten

        return new_T

