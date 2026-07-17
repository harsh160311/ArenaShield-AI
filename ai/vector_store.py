import json
import os
import numpy as np
import pickle
import re

BASE = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE, "..", "data", "stadium_embeddings.pkl")
STADIUMS_PATH = os.path.join(BASE, "..", "data", "stadiums.json")


def _char_ngrams(text, n=3):
    text = text.lower()
    return set(text[i:i + n] for i in range(len(text) - n + 1))


def _text_to_vector(text, vocab):
    ngrams = _char_ngrams(text)
    vec = np.zeros(len(vocab), dtype=np.float32)
    for i, gram in enumerate(vocab):
        if gram in ngrams:
            vec[i] = 1.0
    return vec


def _build_vocab(texts, n=3):
    vocab = set()
    for t in texts:
        vocab.update(_char_ngrams(t, n))
    return sorted(vocab)


def cosine_similarity(a, b):
    dot = float(np.dot(a, b))
    norm_a = float(np.linalg.norm(a))
    norm_b = float(np.linalg.norm(b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class VectorStore:
    def __init__(self, index_path=INDEX_PATH):
        self.index_path = index_path
        self.embeddings = []
        self.metadata = []
        self.vocab = []
        self.dimension = 0
        self._load_or_build()

    def _load_or_build(self):
        if os.path.exists(self.index_path):
            try:
                with open(self.index_path, "rb") as f:
                    data = pickle.load(f)
                self.embeddings = data["embeddings"]
                self.metadata = data["metadata"]
                self.vocab = data["vocab"]
                self.dimension = data["dimension"]
                return
            except Exception:
                pass
        self._build_index()

    def _build_index(self):
        texts = []
        metadata = []
        stadiums_data = self._load_stadiums()
        for s in stadiums_data:
            name = s.get("name", "")
            location = s.get("location", "")
            country = s.get("country", "")
            text = f"{name} {location} {country}"
            texts.append(text)
            metadata.append({
                "id": s.get("id"),
                "name": name,
                "location": location,
                "country": country,
                "capacity": s.get("capacity", 0),
            })

        self.vocab = _build_vocab(texts)
        self.dimension = len(self.vocab)
        self.embeddings = []
        self.metadata = metadata

        for t in texts:
            self.embeddings.append(_text_to_vector(t, self.vocab))

        self.embeddings = np.array(self.embeddings, dtype=np.float32)
        self._save_index()

    def _load_stadiums(self):
        try:
            with open(STADIUMS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("stadiums", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_index(self):
        try:
            with open(self.index_path, "wb") as f:
                pickle.dump({
                    "embeddings": self.embeddings,
                    "metadata": self.metadata,
                    "vocab": self.vocab,
                    "dimension": self.dimension,
                }, f)
        except Exception:
            pass

    def search(self, query, top_k=5):
        if self.dimension == 0 or len(self.embeddings) == 0:
            return []
        query_vec = _text_to_vector(query, self.vocab)
        scores = []
        for i, vec in enumerate(self.embeddings):
            sim = cosine_similarity(query_vec, vec)
            scores.append((sim, i))
        scores.sort(key=lambda x: x[0], reverse=True)
        results = []
        for sim, idx in scores[:top_k]:
            if sim > 0:
                results.append({**self.metadata[idx], "score": round(sim, 4)})
        return results
