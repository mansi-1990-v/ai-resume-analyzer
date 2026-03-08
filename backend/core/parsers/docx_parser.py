import docx
from backend.core.parsers.base import BaseParser

class DocxParser(BaseParser):
    def parse(self, file_path: str) -> str:
        """
        Parses a DOCX file and returns raw text.
        """
        text = ""
        try:
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            raise Exception(f"Failed to parse DOCX: {str(e)}")
        
        return text
