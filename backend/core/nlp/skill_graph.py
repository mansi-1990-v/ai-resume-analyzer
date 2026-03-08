import faiss
import pickle
import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

class SemanticSkillGraph:
    def __init__(self, index_path='models/skills.index', mapping_path='models/skills_mapping.pkl'):
        # Lazy load model
        self.model = None
        try:
            self.index = faiss.read_index(index_path)
            with open(mapping_path, 'rb') as f:
                self.skills_mapping = pickle.load(f)
        except Exception:
            self.index = None
            self.skills_mapping = None

    def _get_model(self):
        if self.model is None:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        return self.model

    def extract_and_normalize(self, raw_skills_text: List[str], threshold: float = 0.6) -> Dict[str, List[str]]:
        """
        Takes raw extracted tokens and aligns them to the standardized skill graph.
        """
        if not raw_skills_text or not self.index:
            return {"technical_skills": [], "soft_skills": [], "tools": []}

        model = self._get_model()
        embeddings = model.encode(raw_skills_text)
        embeddings = np.array(embeddings).astype('float32')
        faiss.normalize_L2(embeddings)

        # Search for top 1 closest skill for each token
        k = 1
        D, I = self.index.search(embeddings, k)

        normalized = {"technical_skills": set(), "soft_skills": set(), "tools": set()}
        
        hierarchy_map = {
            "React": ["JavaScript", "Frontend Development"],
            "Angular": ["TypeScript", "JavaScript", "Frontend Development"],
            "Django": ["Python", "Backend Development"],
            "FastAPI": ["Python", "Backend Development", "API"],
            "PyTorch": ["Machine Learning", "Python", "Deep Learning"],
            "TensorFlow": ["Machine Learning", "Python", "Deep Learning"],
            "Pandas": ["Python", "Data Analysis"],
            "Node.js": ["JavaScript", "Backend Development"],
            "Spring Boot": ["Java", "Backend Development"],
            "AWS": ["Cloud Computing", "DevOps"],
            "Docker": ["DevOps", "Containerization"]
        }
        
        for i, (dist, idx) in enumerate(zip(D, I)):
            if dist[0] >= threshold:
                matched_skill = self.skills_mapping[idx[0]]
                category = matched_skill['category']
                name = matched_skill['name']
                
                # Broadly categorize into technical, soft, or tools based on subset logic
                if category in ["Programming Language", "Frontend Framework", "Backend Framework", "Database", "AI/NLP", "Machine Learning Framework", "Message Queue", "Architecture", "API", "Cloud Computing"]:
                    normalized["technical_skills"].add(name)
                    if name in hierarchy_map:
                        for implicit in hierarchy_map[name]:
                            normalized["technical_skills"].add(implicit)
                elif category in ["Design Tool", "Data Analysis Tool", "Data Visualization", "DevOps"]:
                    normalized["tools"].add(name)
                    if name in hierarchy_map:
                        for implicit in hierarchy_map[name]:
                            normalized["tools"].add(implicit)
                else:
                    normalized["soft_skills"].add(name) # Fallback or methodology

        return {
            "technical_skills": list(normalized["technical_skills"]),
            "soft_skills": list(normalized["soft_skills"]),
            "tools": list(normalized["tools"])
        }
