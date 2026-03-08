from backend.core.parsers.base import BaseParser

class TXTParser(BaseParser):
    def parse(self, file_path: str) -> str:
        """
        Reads a TXT file and returns raw text.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Failed to parse TXT: {str(e)}")
