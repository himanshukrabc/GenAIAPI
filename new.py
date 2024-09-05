# wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/examples/data/10q/uber_10q_march_2022.pdf' -O './data/uber_10q_march_2022.pdf'
# wget "https://meetings.wmo.int/Cg-19/PublishingImages/SitePages/FINAC-43/7%20-%20EC-77-Doc%205%20Financial%20Statements%20for%202022%20(FINAC).pptx" -O './data/presentation.pptx'
import os
import nest_asyncio  # noqa: E402
nest_asyncio.apply()
from dotenv import load_dotenv
load_dotenv()

from llama_parse import LlamaParse
llamaparse_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
import pickle
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
import qdrant_client

qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

from llama_index.embeddings.fastembed import FastEmbedEmbedding
""" embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    #model_name="llama2",
    base_url="http://localhost:11434",
    ollama_additional_kwargs={"mirostat": 0},
) """

from llama_index.core import Settings
from llama_index.llms.groq import Groq
groq_api_key = os.getenv("GROQ_API_KEY")

class SRTModel:
    def __init__(self):
        self.load_or_parse_data()
        """ embed_model = OllamaEmbedding(
            model_name="nomic-embed-text",
            #model_name="llama2",
            base_url="http://localhost:11434",
            ollama_additional_kwargs={"mirostat": 0},
        ) """
        self.Settings=Settings
        self.Settings.embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")
        self.Settings.llm = Groq(model="mixtral-8x7b-32768", api_key=groq_api_key)
        self.client = qdrant_client.QdrantClient(api_key=qdrant_api_key, url=qdrant_url,)
        self.vector_store = QdrantVectorStore(client=self.client, collection_name='doc_doc')
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        self.index = VectorStoreIndex.from_documents(documents=self.parsed_data, storage_context=self.storage_context, show_progress=True)
        self.query_engine=self.index.as_query_engine()


    # Define a function to load parsed data if available, or parse if not
    def load_or_parse_data(self):
        data_file = "./data_doc/parsed_data_1.pkl"
        if os.path.exists(data_file):
            with open(data_file, "rb") as f:
                parsed_data = pickle.load(f)
        else:
            dir_list = os.listdir("./data")
            for i in range(0,len(dir_list)):
                dir_list[i]="./data/"+ dir_list[i]
            print(dir_list)
            llama_parse_documents = LlamaParse(api_key=llamaparse_api_key, result_type="markdown").load_data(dir_list)
            with open(data_file, "wb") as f:
                pickle.dump(llama_parse_documents, f)
            parsed_data = llama_parse_documents
        self.parsed_data = parsed_data

    def run(self,q):
        return self.query_engine.query(q)