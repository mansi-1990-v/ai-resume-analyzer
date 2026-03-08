import faiss
import pickle
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from backend.core.schemas import RolePrediction

class RolePredictor:
    def __init__(self, index_path='models/roles.index', mapping_path='models/roles_mapping.pkl'):
        self.model = None
        try:
            self.index = faiss.read_index(index_path)
            with open(mapping_path, 'rb') as f:
                self.roles_mapping = pickle.load(f)
        except Exception:
            self.index = None
            self.roles_mapping = None

    def _get_model(self):
        if self.model is None:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        return self.model

    def predict(self, resume_text: str, top_k: int = 3) -> List[RolePrediction]:
        if not self.index or not resume_text:
            return []

        # Summarize resume to prevent embedding truncation issues (max 512 tokens for MiniLM, usually sufficient for dense keywords)
        summarized_text = resume_text[:2000] 
        
        model = self._get_model()
        embedding = model.encode([summarized_text])
        embedding = np.array(embedding).astype('float32')
        faiss.normalize_L2(embedding)

        D, I = self.index.search(embedding, top_k)

        predictions = []
        for dist, idx in zip(D[0], I[0]):
            role_name = self.roles_mapping[idx]['role']
            confidence = round(float(dist) * 100, 2)
            
            # Penalize highly distant vectors
            if confidence > 30.0:
                 predictions.append(RolePrediction(role=role_name, confidence=confidence))

        return predictions
