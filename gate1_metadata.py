
from PIL import Image, ImageChops, ImageEnhance
import io
import numpy as np

def analyze_metadata(image: Image.Image):
    exif = image.getexif()
    gray = np.asarray(image.convert("L"), dtype=np.float32)
    edge_variation = (
        np.abs(np.diff(gray, axis=1)).mean()
        + np.abs(np.diff(gray, axis=0)).mean()
    )
    texture = min(100, round(edge_variation * 2.2))
    review = len(exif) == 0 or texture > 45
    return {
        "status": "REVIEW" if review else "PASS",
        "detail": f"EXIF tags: {len(exif)} • texture indicator: {texture}/100 • resolution: {image.width}×{image.height}",
        "review": review,
    }

def ela_image(image: Image.Image, quality=90):
    buf = io.BytesIO()
    image.convert("RGB").save(buf, "JPEG", quality=quality)
    buf.seek(0)
    compressed = Image.open(buf).convert("RGB")
    diff = ImageChops.difference(image.convert("RGB"), compressed)
    maximum = max(v[1] for v in diff.getextrema()) or 1
    return ImageEnhance.Brightness(diff).enhance(255 / maximum)
