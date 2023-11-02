from llama_cpp import Llama
import os

class LLM():
    model = None
    def __init__(self):
        pass
    
    def complete(self, text):
        pass


class LLMLlama(LLM):
    def __init__(self, model_path=""):
        self.model = Llama(model_path=model_path, embedding=True, n_ctx=2048)
        self.config = {}
        self.config['model_name'] = os.path.basename(model_path)

    def complete(self, text):
        return self.model(text)
    
    def embed(self, text):
        return self.model.embed(text)