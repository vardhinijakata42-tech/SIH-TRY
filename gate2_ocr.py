"""
GATE 2: Computer Vision & Layout OCR
--------------------------------------
1. extract_text()      -> reads all visible text from the document image
2. find_mrz_lines()    -> looks for passport-style MRZ lines (rows of << characters)
3. validate_document() -> simple rule-based checks (does the data look well-formed?)
"""

import pytesseract
from PIL import Image
import re


def extract_text(image_path):
    """
    Runs OCR on the image and returns all detected text as one block.
    Uses Tesseract OCR (installed via packages.txt on the server).
    """
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()


def find_mrz_lines(text):
    """
    Passports have a special 2-line 'Machine Readable Zone' at the bottom,
    made of capital letters, numbers, and '<' fill characters, e.g.:
        P<INDDOE<<JOHN<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        1234567890IND9001014M3001014<<<<<<<<<<<<<<08

    This function scans the OCR text for lines that look like this pattern.
    """
    lines = text.splitlines()
    mrz_lines = [line for line in lines if re.match(r"^[A-Z0-9<]{20,}$", line.replace(" ", ""))]
    return mrz_lines


def validate_document(text):
    """
    Basic rule-based checks on the extracted text. Returns a list of
    (check_name, passed_bool, detail) tuples.
    This is intentionally simple — real systems use official field-format
    rules per document/country.
    """
    results = []

    # Check 1: does the text contain a date-like pattern (DD/MM/YYYY or similar)?
    has_date = bool(re.search(r"\b\d{2}[/\-.]\d{2}[/\-.]\d{2,4}\b", text))
    results.append(("Contains a recognizable date", has_date,
                     "Looks for a DOB/expiry-style date pattern."))

    # Check 2: does the text contain something that looks like a document number?
    has_doc_number = bool(re.search(r"\b[A-Z0-9]{6,12}\b", text.upper()))
    results.append(("Contains a document-number-like pattern", has_doc_number,
                     "Looks for a 6-12 character alphanumeric code."))

    # Check 3: MRZ presence (passports only)
    mrz_lines = find_mrz_lines(text)
    results.append(("MRZ (machine-readable zone) detected", len(mrz_lines) >= 1,
                     f"Found {len(mrz_lines)} MRZ-like line(s)."))

    return results
