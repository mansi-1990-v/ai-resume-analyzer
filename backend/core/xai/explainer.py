from typing import List
from backend.core.schemas import ScoreBreakdown

class ExplainableAIEngine:
    def generate_explanation(self, jd_skills: List[str], res_skills: List[str], breakdown: ScoreBreakdown, evidences: List[str]) -> str:
        """
        Generates a human-friendly paragraph explaining the 'Why' behind a job fit score.
        Uses exact contextual evidences scraped via RAG chunking.
        """
        
        has_skills = set(res_skills)
        needed_skills = set(jd_skills)
        missing = list(needed_skills - has_skills)
        matched = list(needed_skills.intersection(has_skills))
        
        explanations = []
        
        if breakdown.skills_match >= 80:
            explanations.append(f"Excellent skill alignment. You possess key requirements like {', '.join(matched[:3])}.")
        elif breakdown.skills_match >= 50:
            explanations.append(f"Moderate skill alignment. You have {len(matched)} matching skills, but you are missing {', '.join(missing[:3])}.")
        else:
            explanations.append(f"Low skill alignment. Consider upskilling in {', '.join(missing[:3])}.")
            
        if breakdown.experience_match >= 80:
            explanations.append("Your overall experience matches the job very closely.")
        elif breakdown.experience_match < 50:
            explanations.append("Your past experience doesn't strongly parallel the core responsibilities described in the job.")
            
        if evidences:
            explanations.append("\n\n**Verified Evidence from your Resume:**\n")
            for idx, ev in enumerate(evidences[:2]):
                explanations.append(f"• \"{ev.strip()}\"")
            
        return " ".join(explanations)
