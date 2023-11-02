def doc_join(str_list):
    return "\ndoc:".join(str_list)

class QueryPlanner:
    def __init__(self, llm, store):
        self.llm = llm
        self.store = store

    def query(self, prompt, n_results=5):

        documents = []
        constructed_prompt_template = f"Answer the question using the provided context. Your answer should be in your own words and be no longer than 50 words. \n\n Context: {doc_join(documents)} \n\n Question: {prompt} \n\n Answer:"
        results = self.store.db.query(
            query_embeddings=self.store.embedder(prompt),
            n_results=n_results,
            include=["documents"],
        )
        documents = results["documents"][0]
        joined_docs = doc_join(documents)
        #if (len(joined_docs) + len(constructed_prompt_template)) > self.llm.model.n_ctx():
        #    pass

        constructed_prompt_template = f"Answer the question using the provided context. Your answer should be in your own words and be no longer than 50 words. \n\n Context: {joined_docs} \n\n Question: {prompt} \n\n Answer:"
        return self.llm.complete(constructed_prompt_template)['choices'][0]['text']
