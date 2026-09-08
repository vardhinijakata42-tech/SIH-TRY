
# DETECT-X Protocol Terminal

Modular Streamlit prototype for a five-gate document verification workflow.

## Files

- `app.py` = main Streamlit interface
- `gate1_metadata.py` = metadata + texture analysis
- `gate2_ocr.py` = OCR/demo format validation
- `gate3_face.py` = biometric integration placeholder
- `requirements.txt` = dependencies
- `assets/` = optional SVG icons/assets

## Streamlit

Main file path:

`app.py`

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Note

This is a demonstration prototype. It does not authenticate identity, access government databases, or prove document fraud. Use only non-sensitive sample images.
