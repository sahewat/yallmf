from typing import List, Union

import chromadb
import xxhash

from tqdm import tqdm

def chunk_list(input_list, n):
    chunked_list = []
    for i in range(0, len(input_list), n):
        chunked_list.append(input_list[i:i + n])
    return chunked_list

class VectorStore():
    def __init__(self, path, embedder, name="", chunk_size=512, type="chroma") -> None:
        self._client = chromadb.PersistentClient(path=path) 
        self.embedder = embedder
        self.config = {}
        self.chunk_size = chunk_size
        if not name:
            name = "default"
        self.config['collection_name'] = name + "_" + embedder.name + "_chunk_" + str(self.chunk_size)
        self.db = self._client.get_or_create_collection(name=self.config['collection_name'], embedding_function=embedder)

    def add(self, text: Union[str, List[str]]):
        if type(text) == str:
            text = [text]
            chunked_text = chunk_list(text, self.chunk_size)
        elif type(text) == list:
            chunked_text = []
            for t in text:
                chunked_text += chunk_list(t, self.chunk_size)
            pass
        else:
            raise TypeError("text must be str or List[str]")
        
        
        hashes = []

        
        for i in tqdm(range(len(chunked_text))):
            chunk = chunked_text[i]
            hash = xxhash.xxh32_hexdigest(chunk)
            does_exist = self.db.get(ids=[hash])
            if does_exist['documents'] and len(does_exist['documents']):
                print("Embedding: {} already exists".format(hash))
                continue
            else:
                embedding = self.embedder(chunk)
                self.db.add(documents=[chunk], embeddings=[embedding], ids=[hash])
                hashes.append(hash)

        return hashes


