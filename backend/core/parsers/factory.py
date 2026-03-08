import os
from ast import operator

from backend.core.parsers.base import BaseParser
from backend.core.parsers.pdf_parser import PDFParser
from backend.core.parsers.docx_parser import DocxParser
from backend.core.parsers.txt_parser import TXTParser

def get_parser(file_path: str) -> BaseParser:
    """
    Returns the appropriate parser based on the file extension.
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext == ".pdf":
        return PDFParser()
    elif ext == ".docx":
        return DocxParser()
    elif ext == ".txt":
        return TXTParser()
    else:
        raise ValueError(f"Unsupported file extension: {ext}")
