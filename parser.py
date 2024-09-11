import os
import nest_asyncio  
nest_asyncio.apply()
from dotenv import load_dotenv
load_dotenv()

from llama_parse import LlamaParse

llamaparse_api_key = os.getenv("LLAMA_CLOUD_API_KEY")
import pickle

def load_or_parse_data():
    data_file = "./data/parsed_data.pkl"
    #seeing if already parsed, we have static files for now
    if os.path.exists(data_file):
        with open(data_file, "rb") as f:
            parsed_data = pickle.load(f)
    else:
        dir_list = os.listdir("./data")
        
        for i in range(0,len(dir_list)):
            dir_list[i]="./data/"+ dir_list[i]
        print(dir_list)
        llama_parse_documents = LlamaParse(api_key=llamaparse_api_key, result_type="markdown").load_data(dir_list) #parsing

       
        with open(data_file, "wb") as f:
            pickle.dump(llama_parse_documents, f)
        
        parsed_data = llama_parse_documents
    
    return parsed_data

llama_parse_documents = load_or_parse_data()
len(llama_parse_documents)

llama_parse_documents[0].text[:100]

type(llama_parse_documents)