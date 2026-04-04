from typing import List, Dict


class CodeRetriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Get relevant code chunks using vector search
        """
        return self.vector_store.search(query, top_k=top_k)