# extractor.py
import fitz  # PyMuPDF
from pdf2image import convert_from_path
import pytesseract

def extract_text_pdf(path, ocr_threshold=200, poppler_path=None, tesseract_cmd=None, ocr_lang=None):
    """
    Extrai texto de PDF. Faz OCR se a extração direta for muito curta.
    - poppler_path: caminho para binários do poppler (Windows), se necessário.
    - tesseract_cmd: caminho absoluto para tesseract.exe (Windows), se necessário.
    - ocr_lang: 'por' ou 'eng' (se tiver instalados)
    """
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    doc = fitz.open(path)
    pages_text = [page.get_text("text") for page in doc]
    full_text = "\n===PAGE===\n".join(pages_text).strip()

    # Se texto extraído for pequeno, tenta OCR
    if len(full_text) < ocr_threshold:
        images = convert_from_path(path, dpi=200, poppler_path=poppler_path)
        ocr_pages = []
        for img in images:
            if ocr_lang:
                ocr_pages.append(pytesseract.image_to_string(img, lang=ocr_lang))
            else:
                ocr_pages.append(pytesseract.image_to_string(img))
        full_text = "\n===PAGE===\n".join(ocr_pages).strip()

    return full_text
