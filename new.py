import os
import nest_asyncio  
nest_asyncio.apply()
from dotenv import load_dotenv
load_dotenv()

from llama_parse import LlamaParse
from llama_index.core import (
    load_index_from_storage,
    load_indices_from_storage,
    load_graph_from_storage,
)

llamaparse_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
import pickle

def load_or_parse_data():
    data_file = "./data/parsed_data.pkl"
    
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
    
    return parsed_data

llama_parse_documents = load_or_parse_data()
len(llama_parse_documents)

llama_parse_documents[0].text[:100]

type(llama_parse_documents)

from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext

import qdrant_client

qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")

from llama_index.embeddings.fastembed import FastEmbedEmbedding
embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")

""" embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    #model_name="llama2",
    base_url="http://localhost:11434",
    ollama_additional_kwargs={"mirostat": 0},
) """

from llama_index.core import Settings

Settings.embed_model = embed_model

from llama_index.llms.groq import Groq
groq_api_key = os.getenv("GROQ_API_KEY")

llm = Groq(model="mixtral-8x7b-32768", api_key=groq_api_key)
Settings.llm = llm

client = qdrant_client.QdrantClient(api_key=qdrant_api_key, url=qdrant_url,)

vector_store = QdrantVectorStore(client=client, collection_name='qdrant_rag')
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents=llama_parse_documents, storage_context=storage_context, show_progress=True)

#### PERSIST INDEX #####
index.storage_context.persist()

storage_context = StorageContext.from_defaults(persist_dir="./storage")

index = load_index_from_storage(storage_context)

# create a query engine for the index
query_engine = index.as_query_engine()

# query the engine
query = "what is the common stock balance as of Balance as of March 31, 2022?"
while(1):
    user_input = input("Enter Query:")
    if user_input == "exit":
        break;
    elif user_input == "new":
        print("Done")
    else :
        response = query_engine.query(user_input)
        print(response)