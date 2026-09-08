"""
GATE 3: Biometric Liveness & Face Verification
--------------------------------------------------
Uses OpenCV only (no heavy deep-learning libraries) so it installs reliably
on free hosting. This makes it a lightweight DEMO version — good enough to
show the concept working, not a production-grade biometric system.

1. detect_face()     -> finds and crops a face in an image
2. compare_faces()   -> gives a similarity score between two face crops
3. check_liveness()  -> simple sharpness-based heuristic (flags flat/printed photos)
"""

import cv2
import numpy as np

# OpenCV ships with a pre-trained face detector, no extra download needed
_face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


def detect_face(image_path):
    """
    Finds the largest face in the image and returns it as a cropped,
    grayscale, resized image (for consistent comparison later).
    Returns None if no face is found.
    """
    image = cv2.imread(image_path)
    if image is None:
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = _face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) == 0:
        return None

    # Pick the largest detected face (most likely the main subject)
    x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
    face_crop = gray[y:y + h, x:x + w]
    face_resized = cv2.resize(face_crop, (200, 200))
    return face_resized


def compare_faces(image_path_1, image_path_2):
    """
    Compares two faces using histogram correlation (a simple, dependency-light
    similarity measure). Returns a similarity score from 0-100 and a match bool.
    """
    face1 = detect_face(image_path_1)
    face2 = detect_face(image_path_2)

    if face1 is None or face2 is None:
        return None, False, "Could not detect a face in one or both images."

    hist1 = cv2.calcHist([face1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([face2], [0], None, [256], [0, 256])
    cv2.normalize(hist1, hist1)
    cv2.normalize(hist2, hist2)

    correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    similarity_score = round(max(correlation, 0) * 100, 2)
    is_match = similarity_score >= 55  # demo threshold, tune as needed

    return similarity_score, is_match, "Compared using histogram correlation (demo method)."


def check_liveness(image_path):
    """
    VERY SIMPLIFIED liveness heuristic for demo purposes:
    - A photo of a photo (printed/screen) tends to be less sharp / have flatter
      texture than a real, live camera capture.
    - We measure image sharpness (Laplacian variance). Very low sharpness is
      flagged as "possibly not live."

    NOTE: real liveness detection uses motion, blink detection, depth sensors,
    or trained anti-spoofing models. This is a placeholder to demonstrate the
    concept, not a secure liveness check.
    """
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return None, "Could not read image."

    sharpness = cv2.Laplacian(image, cv2.CV_64F).var()
    likely_live = sharpness > 50  # demo threshold

    return likely_live, f"Sharpness score: {round(sharpness, 2)} (demo heuristic)."
