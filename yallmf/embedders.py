from typing import List

from fast_sentence_transformers import FastSentenceTransformer as SentenceTransformer

class Embedder():
    def __init__(self, embed_fn, embed_name):
        self._embed = embed_fn
        self.name = embed_name
    def __call__(self, text):
        return self._embed(text)

class SentenceTransformerEmbedder():
    def __init__(self, name="all-MiniLM-L6-v2"):
        # use any sentence-transformer
        self._encoder = SentenceTransformer(name, device="cpu", quantize=False)
        self.name = name

    def _embed(self, text) -> List[float]:
        return self._encoder.encode(text).tolist()

    def __call__(self, text):
        return self._embed(text)


