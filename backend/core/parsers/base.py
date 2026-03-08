from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> str:
        """
        Parses a document and returns the extracted raw text.
        """
        pass
