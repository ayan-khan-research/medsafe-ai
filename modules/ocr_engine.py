import io
import re
from typing import List

from PIL import Image


def extract_text_from_image(uploaded_file) -> str:
    """Tries OCR using easyocr. Falls back gracefully if unavailable."""
    try:
        import easyocr  # type: ignore

        image = Image.open(uploaded_file).convert('RGB')
        reader = easyocr.Reader(['en'], gpu=False)
        result = reader.readtext(image, detail=0)
        text = ' '.join(result).strip()
        if text:
            return text
    except Exception:
        pass

    # Fallback for demo when OCR dependency or model download fails
    uploaded_file.seek(0)
    return 'OCR could not run in this environment. Demo fallback: type medicine names manually or use a clearer image.'


def extract_medicines_from_text(text: str, med_db) -> List[str]:
    found = []
    lowered = text.lower()
    for med in med_db.keys():
        if re.search(rf'\b{re.escape(med)}\b', lowered):
            found.append(med)
    return sorted(set(found))
