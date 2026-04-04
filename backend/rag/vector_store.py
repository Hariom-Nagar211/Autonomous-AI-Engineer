import os
import faiss
import numpy as np
from typing import List, Dict
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

# FAISS : Library for efficient similarity search and only store embeddings in memory, not the original code text.

class VectorStore:
    def __init__(self):
        # Load local embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        self.dim = 384  # embedding size for this model
        self.index = faiss.IndexFlatIP(self.dim)
        self.metadata = []

    def get_embedding(self, text: str) -> List[float]:
        """
        Generate embedding using local model
        """
        return self.model.encode(text[:2000]).tolist()

    def build_index(self, parsed_data: List[Dict]):
        embeddings = []

        print("🔄 Generating embeddings...")

        for item in tqdm(parsed_data):
            try:
                emb = self.get_embedding(item["code"])
                embeddings.append(emb)
                self.metadata.append(item)
            except Exception as e:
                print("❌ Error:", e)

        embeddings = np.array(embeddings).astype("float32")

        print("⚡ Adding to FAISS index...")
        self.index.add(embeddings)

        print(f"✅ Indexed {len(self.metadata)} code chunks")

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        query_emb = np.array(
            [self.get_embedding(query)]
        ).astype("float32")

        distances, indices = self.index.search(query_emb, top_k)

        results = []
        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results