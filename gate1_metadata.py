"""
GATE 1: Metadata & Textural Analysis
--------------------------------------
3 functions:
1. extract_metadata()    -> reads hidden EXIF info (camera, date, GPS)
2. perform_ela()         -> highlights edited/pasted regions (Error Level Analysis)
3. detect_noise_anomaly()-> finds unusually smooth regions (splicing/inpainting sign)
"""

from PIL import Image, ImageChops, ExifTags
import numpy as np
import cv2
import io


def extract_metadata(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif() if hasattr(image, "_getexif") else None

    if exif_data is None:
        return {"info": "No EXIF metadata found. Common for edited, screenshotted, "
                         "or re-saved images."}

    metadata = {}
    for tag_id, value in exif_data.items():
        tag_name = ExifTags.TAGS.get(tag_id, tag_id)
        metadata[tag_name] = value
    return metadata


def perform_ela(image_path, quality=90):
    original = Image.open(image_path).convert("RGB")

    buffer = io.BytesIO()
    original.save(buffer, "JPEG", quality=quality)
    buffer.seek(0)
    recompressed = Image.open(buffer)

    ela_image = ImageChops.difference(original, recompressed)

    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema]) or 1
    scale_factor = 255.0 / max_diff
    ela_image = ela_image.point(lambda p: p * scale_factor)

    return ela_image


def detect_noise_anomaly(image_path, block_size=16):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError("Could not read image.")

    h, w = image.shape
    heatmap = np.zeros((h, w), dtype=np.float32)

    noise_values = []
    coordinates = []

    for y in range(0, h - block_size, block_size):
        for x in range(0, w - block_size, block_size):
            block = image[y:y + block_size, x:x + block_size]
            noise_level = cv2.Laplacian(block, cv2.CV_64F).var()
            noise_values.append(noise_level)
            coordinates.append((y, x))

    if not noise_values:
        return None, 0

    noise_values = np.array(noise_values)
    mean_noise = noise_values.mean()
    std_noise = noise_values.std() or 1

    suspicious_blocks = 0
    for (y, x), noise_level in zip(coordinates, noise_values):
        z_score = (mean_noise - noise_level) / std_noise
        if z_score > 1.5:
            heatmap[y:y + block_size, x:x + block_size] = 255
            suspicious_blocks += 1
        else:
            heatmap[y:y + block_size, x:x + block_size] = 0

    risk_score = round((suspicious_blocks / len(noise_values)) * 100, 2)
    heatmap_image = Image.fromarray(heatmap.astype(np.uint8))
    return heatmap_image, risk_score
