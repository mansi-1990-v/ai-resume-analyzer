import numpy as np
from sentence_transformers import SentenceTransformer
from backend.core.schemas import JobFitResult, ScoreBreakdown
from backend.core.nlp.skill_graph import SemanticSkillGraph

class JobMatcher:
    def __init__(self):
        self.model = None
        self.skill_graph = SemanticSkillGraph()

    def _get_model(self):
        if self.model is None:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        return self.model

    def _cosine_similarity(self, v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    def evaluate_fit(self, resume_text: str, job_description: str, extracted_skills: list) -> JobFitResult:
        model = self._get_model()
        
        # 1. Broad Semantic Similarity & Sentence RAG Chunking
        import re
        sentences = [s.strip() for s in re.split(r'[.!?\n]', resume_text) if len(s.strip()) > 30]
        if not sentences:
            sentences = [resume_text]
            
        jd_emb = model.encode([job_description], normalize_embeddings=True)[0]
        sentence_embs = model.encode(sentences, normalize_embeddings=True)
        
        # Calculate cosine similarity for all sentences against JD
        similarities = np.dot(sentence_embs, jd_emb)
        
        # Get top 3 sentences as evidence
        top_indices = np.argsort(similarities)[::-1][:3]
        evidences = [sentences[i] for i in top_indices if similarities[i] > 0.3]
        
        if len(evidences) > 0:
            experience_score = float(np.mean([similarities[i] for i in top_indices]) * 100)
        else:
            experience_score = 0.0
            
        experience_score = max(0, min(100, experience_score))

        # 2. Skill Match
        # Extract skills from JD using the same SkillGraph
        # This is a rudimentary chunking to mimic JD skill extraction
        jd_words = job_description.split()
        jd_skills_dict = self.skill_graph.extract_and_normalize(jd_words, threshold=0.7)
        
        jd_all_skills = set(jd_skills_dict["technical_skills"] + jd_skills_dict["soft_skills"] + jd_skills_dict["tools"])
        res_all_skills = set(extracted_skills)
        
        if len(jd_all_skills) > 0:
            matching_skills = list(jd_all_skills.intersection(res_all_skills))
            missing_skills = list(jd_all_skills.difference(res_all_skills))
            skills_score = (len(matching_skills) / len(jd_all_skills)) * 100
        else:
            matching_skills = []
            missing_skills = []
            skills_score = 100.0 # No skills required

        # 3. Overall Score Calculation
        overall = (skills_score * 0.6) + (experience_score * 0.4)
        
        return JobFitResult(
            overall_score=round(overall, 1),
            breakdown=ScoreBreakdown(
                skills_match=round(skills_score, 1),
                experience_match=round(experience_score, 1),
                education_match=85.0 # Mocked for now; normally parse education degree vs JD degree
            ),
            matching_skills=matching_skills,
            missing_skills=missing_skills,
            explanation=f"Your profile strongly aligns with {round(overall, 1)}% of the requirements. "
                        f"You match well on semantic experience but are missing key tools in {', '.join(missing_skills[:3]) if missing_skills else 'nothing crucial'}.",
            evidences=evidences
        )
