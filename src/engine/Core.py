import re
from collections import Counter
from typing import Dict, List, Tuple
import numpy as np
from nltk.stem import SnowballStemmer

LANGUAGE = SnowballStemmer.languages

class Piper:
    def __init__(self) -> None:
        self.invert_index: Dict[str, Dict[str, int]] = {}
        self.terms: List[str] = []
        self.document_ids = set()
        self.vector_space = dict()

    def clear(self) -> None:
        self.invert_index.clear()
        self.terms = []
        self.document_ids.clear()

    @staticmethod
    def _tokenize_and_stem(plaintext: str, language: str) -> List[str]:
        stemmer = SnowballStemmer(language=language)
        tokens = re.findall(r"\w+", plaintext.lower(), flags=re.UNICODE)
        stems = [stemmer.stem(tok) for tok in tokens if tok.strip() != ""]
        return stems

    def index(self, document_id: str, plaintext: str, leng: str) -> None:
        stems = self._tokenize_and_stem(plaintext, leng)
        if not stems:
            return

        counts = Counter(stems)
        for term, freq in counts.items():
            if term not in self.invert_index:
                self.invert_index[term] = {}
            self.invert_index[term][document_id] = freq

        self.document_ids.add(document_id)
        self.terms = sorted(self.invert_index.keys())

    def compute_vector(self, plaintext: str, leng: str) -> np.ndarray:
        N = len(self.document_ids)
        stems = self._tokenize_and_stem(plaintext, leng)
        query_counts = Counter(stems)

        vec = np.zeros(len(self.terms), dtype=float)

        for i, term in enumerate(self.terms):
            tf = query_counts.get(term, 0)
            if tf > 0:
                tf_weight = 1.0 + np.log2(tf)
            else:
                tf_weight = 0.0

            df = len(self.invert_index.get(term, {}))
            idf = np.log2((1.0 + max(1, N)) / (1.0 + df))

            vec[i] = tf_weight * idf


        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm

        return vec

    def search(self, query_vector) -> Dict[str, int]:
        search_result = dict()
        for document_id, vector in self.vector_space.items():
            search_result[document_id] = np.linalg.norm(query_vector - vector).__float__()
        return search_result.items()

# if __name__ == "__main__":
#     p = Piper()
#     content = [
#         {"document_id": "doc1", "content": "Hola, mundo! Hola a todos.", "leng": "spanish"},
#         {"document_id": "doc2", "content": "Mundo de pruebas y ejemplos.", "leng": "spanish"}
#     ]

#     for row in content:
#         p.index(row["document_id"], row["content"], row["leng"])
    
#     # compute all vector
#     for row in content:
#         document_vector = p.compute_vector(row["content"], row["leng"])
#         p.vector_space[row["document_id"]] = document_vector

#     q_vec = p.compute_vector("pruebas y ejemplos", "spanish")
#     for document_id, rank in p.search(q_vec):
#         print(document_id, rank)