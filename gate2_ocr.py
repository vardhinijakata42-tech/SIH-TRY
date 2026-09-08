
import re

def analyze_ocr(text):
    if not text.strip():
        return {
            "status": "AWAITING",
            "detail": "Paste OCR output to run the demo format rule.",
            "review": False,
        }

    # Generic demo rule only. It does not validate an actual government record.
    grouped_12 = bool(re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", text))
    return {
        "status": "PASS" if grouped_12 else "REVIEW",
        "detail": "12-digit grouped-number pattern detected." if grouped_12 else "Expected demo pattern not detected.",
        "review": not grouped_12,
    }
