import fitz  # PyMuPDF
from backend.core.parsers.base import BaseParser

class PDFParser(BaseParser):
    def parse(self, file_path: str) -> str:
        """
        Parses a PDF file using PyMuPDF to retain layout and return raw text.
        """
        text = ""
        try:
            with fitz.open(file_path) as doc:
                for page in doc:
                    text += page.get_text() + "\n"
        except Exception as e:
            raise Exception(f"Failed to parse PDF: {str(e)}")
        
        return text
