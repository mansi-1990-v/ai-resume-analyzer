import re
import spacy
from typing import List, Dict, Any, Optional

class EntityExtractor:
    def __init__(self):
        # Load the English NLP model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Fallback if not downloaded yet
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")

    def extract_email(self, text: str) -> Optional[str]:
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else None

    def extract_phone(self, text: str) -> Optional[str]:
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        matches = re.findall(phone_pattern, text)
        return matches[0] if matches else None

    def extract_links(self, text: str) -> List[str]:
        link_pattern = r'(https?://[^\s]+|www\.[^\s]+|linkedin\.com/in/[^\s]+|github\.com/[^\s]+)'
        matches = re.findall(link_pattern, text)
        return list(set(matches))

    def extract_name(self, text: str) -> Optional[str]:
        doc = self.nlp(text[:2000]) # Usually name is at the top
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
        return None

    def extract_all(self, text: str) -> Dict[str, Any]:
        return {
            "name": self.extract_name(text),
            "email": self.extract_email(text),
            "phone": self.extract_phone(text),
            "links": self.extract_links(text)
        }
