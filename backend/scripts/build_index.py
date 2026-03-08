import json
import os
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

def load_json(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def build_skills_index(model):
    print("Building skills index...")
    skills = load_json('data/skills_database.json')
    skill_names = [s['name'] for s in skills]
    
    embeddings = model.encode(skill_names, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')
    
    # L2 Normalized for Cosine Similarity
    faiss.normalize_L2(embeddings)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension) # Inner Product -> Cosine Similarity if normalized
    index.add(embeddings)
    
    faiss.write_index(index, 'models/skills.index')
    with open('models/skills_mapping.pkl', 'wb') as f:
        pickle.dump(skills, f)
    print("Skills index built successfully.")

def build_roles_index(model):
    print("Building roles index...")
    roles = load_json('data/roles_database.json')
    role_texts = [r['role'] + " " + r['description'] for r in roles]
    
    embeddings = model.encode(role_texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')
    
    faiss.normalize_L2(embeddings)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    
    faiss.write_index(index, 'models/roles.index')
    with open('models/roles_mapping.pkl', 'wb') as f:
        pickle.dump(roles, f)
    print("Roles index built successfully.")

if __name__ == "__main__":
    os.makedirs('models', exist_ok=True)
    print("Loading SentenceTransformer model...")
    # Using a fast, small model for quick semantic search
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    build_skills_index(model)
    build_roles_index(model)
    print("Model and indices saved successfully.")
