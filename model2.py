import pickle
from transformers import pipeline
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
import os
from llama_index.embeddings.fastembed import FastEmbedEmbedding
import qdrant_client
from llama_index.core import Settings
from llama_index.llms.groq import Groq
# Define the LLM Model Agent
class LLMModelAgent:
    def __init__(self, data, model_name):
        self.model = pipeline("text-generation", model=model_name)
        with open(data, "rb") as f:
            llama_parse_documents  = pickle.load(f)
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")
        embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")
        Settings.embed_model = embed_model
        groq_api_key = os.getenv("GROQ_API_KEY")

        llm = Groq(model="mixtral-8x7b-32768", api_key=groq_api_key)
        Settings.llm = llm

        client = qdrant_client.QdrantClient(api_key=qdrant_api_key, url=qdrant_url,)

        vector_store = QdrantVectorStore(client=client, collection_name='qdrant_rag')
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(documents=llama_parse_documents, storage_context=storage_context, show_progress=True)
        self.query_engine = index.as_query_engine()
    
    def query(self, prompt):
        return self.query_engine.query(prompt)    

# Define the Summarization Agent
class SummarizationAgent:
    def __init__(self, model_name):
        self.model = pipeline("summarization", model=model_name)

    def summarize_text(self, text):
        output = self.model(text)
        return output[0]["summary_text"]

# Define the LangChain
class LangChain:
    def __init__(self, llm_model_name, summary_model_name):
        self.sr_agent = LLMModelAgent("./data/parsed_data.pkl",llm_model_name)
        self.doc_agent = LLMModelAgent("./data_doc/parsed_data.pkl",llm_model_name)
        self.summary_agent = SummarizationAgent(summary_model_name)

    def run(self, prompt):
        text = self.sr_agent.query(prompt)
        text2= self.doc_agent.query(prompt)
        print(text)
        print("----------------------------------------------------------------")
        print(text2)
        summary = self.summary_agent.summarize_text(text.response+text2.response)
        return summary
            