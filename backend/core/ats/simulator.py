import re
from typing import List, Dict, Any

class ATSSimulator:
    def evaluate(self, text: str) -> Dict[str, Any]:
        """
        Simulates how an ATS reads a resume.
        Looks for standard section headers, action verbs, and structural integrity.
        """
        score = 100
        suggestions = []
        
        # 1. Section Header Detection
        headers = ["education", "experience", "projects", "skills", "summary"]
        text_lower = text.lower()
        found_headers = [h for h in headers if h in text_lower]
        
        if len(found_headers) < 3:
            score -= 20
            suggestions.append("Missing clear standard sections (e.g., 'Experience', 'Education', 'Skills').")
            
        # 2. Action Verbs Check
        action_verbs = ["developed", "managed", "led", "created", "designed", "improved", "increased", "reduced"]
        verb_count = sum(1 for verb in action_verbs if verb in text_lower)
        
        if verb_count < 3:
            score -= 10
            suggestions.append("Use more strong action verbs (e.g., 'Led', 'Developed', 'Improved') to start bullet points.")
            
        # 3. Quantifiable Impact Check
        numbers = re.findall(r'\b\d{1,3}(?:,\d{3})*(?:\.\d+)?%?\b', text)
        if len(numbers) < 2:
            score -= 15
            suggestions.append("Lack of quantifiable metrics. Try adding numbers or percentages to your achievements.")
            
        # 4. Length / Word Count Check
        word_count = len(text.split())
        if word_count < 200:
            score -= 10
            suggestions.append("Resume is too brief. Add more descriptive bullet points.")
        elif word_count > 1000:
            score -= 5
            suggestions.append("Resume might be too wordy. Keep it concise (under 2 pages).")

        return {
            "ats_score": max(0, score),
            "suggestions": suggestions
        }
