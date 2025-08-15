from typing import Tuple
import os
import fitz  # PyMuPDF
from docx import Document

def _read_pdf(path: str) -> str:
    text = []
    with fitz.open(path) as doc:
        for page in doc:
            text.append(page.get_text())
    return "\n".join(text)

def _read_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def _read_txt(path: str) -> str:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def extract_text(path: str) -> Tuple[str, str]:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':  return _read_pdf(path), ext
    if ext == '.docx': return _read_docx(path), ext
    if ext == '.txt':  return _read_txt(path), ext
    raise ValueError(f'Unsupported file format: {ext}')
