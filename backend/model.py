import pickle
import langgraph._api
import langgraph.graph
import torch
from transformers import pipeline
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import VectorStoreIndex, StorageContext
import os
from llama_index.embeddings.fastembed import FastEmbedEmbedding
import qdrant_client
from llama_index.core import Settings
from llama_index.llms.groq import Groq
import langgraph
import json

#The parsed files data stored in .pkl files
SR_FILES_PATH="./data/parsed_data.pkl"
DOC_FILES_PATH="./data_doc/parsed_data_1.pkl"

LRU_THRESHOLD = 3 #can change this when required, maintains context

class ModelState:
    def __init__(self):
        self.state = dict()
        self.flush_context()
    def update_contexts(self):
        if len(self.state["sr_context"]) == LRU_THRESHOLD:
            self.state["sr_context"].pop(0) 
        if len(self.state["doc_context"]) == LRU_THRESHOLD:
            self.state["doc_context"].pop(0)
        if len(self.state["user_context"]) == LRU_THRESHOLD:
            self.state["user_context"].pop(0)
        
        #maintaining state manually
        self.state["user_context"].append(self.state["prompt"]) 
        self.state["doc_context"].append(self.state["doc_response"])
        self.state["sr_context"].append(self.state["sr_response"])
    def flush_context(self):
        self.state["doc_context"], self.state["sr_context"], self.state["user_context"], self.state["sr_response"], self.state["doc_response"], self.state["prompt"] = [], [], [], [], [], []


class LLMModelAgent:
    def __init__(self, data, model_name,collection):
        self.model = pipeline("text-generation", model=model_name)
        with open(data, "rb") as f:
            llama_parse_documents  = pickle.load(f)
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")  #Qdrant is out vector database
        embed_model = FastEmbedEmbedding(model_name="BAAI/bge-base-en-v1.5")
        Settings.embed_model = embed_model
        groq_api_key = os.getenv("GROQ_API_KEY")
        #using llm model
        llm = Groq(model="mixtral-8x7b-32768", api_key=groq_api_key)
        Settings.llm = llm

        client = qdrant_client.QdrantClient(api_key=qdrant_api_key, url=qdrant_url,)

        vector_store = QdrantVectorStore(client=client, collection_name=collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_documents(documents=llama_parse_documents, storage_context=storage_context, show_progress=True)
        self.query_engine = index.as_query_engine()
        

    def generate_text(self, prompt):
        response = self.query_engine.query(prompt)  #query engine takes in query, did not use chat engine as it is very heavy
        return response
    

class SummarizationAgent:
    def __init__(self, model_name):
        self.model = pipeline("summarization", model=model_name)

    def summarize_text(self, text):
        output = self.model(text)
        return output[0]["summary_text"]

#stores state for SR citations
class SRCitationAgent:
    def __init__(self):
        self.agent = LLMModelAgent(SR_FILES_PATH,"t5-small",'qdrant_rag')
    def get_citation(self,response):
        citation = self.agent.generate_text(response.source_nodes[0].node.text + "Return me the bug number as bug_number, sr id as sr_id and doc Id as doc_id in the following text in json string format. If no such thing is found the send me null in each property.")
        resp = json.loads(citation.response)
        print(resp)
        if(citation.source_nodes[0].score<0.8) or (resp["bug_number"]==None and resp["sr_id"]==None and resp["doc_id"]==None):
            return None
        else:
            return resp

class DocCitationAgent:
    def __init__(self):
        self.agent = LLMModelAgent(DOC_FILES_PATH,"t5-small",'doc_ind')
    def get_citation(self,response):
        return None
        citation = self.agent.generate_text(response.source_nodes[0].node.text + "Return me the link as doc_link in the following text in json string format. If no such thing is found the send me null in each property.")
        resp = json.loads(citation.response)
        print(resp)
        if(citation.source_nodes[0].score<0.4):
            return None
        else:
            return resp

# Execute the workflow
class Model:   
    def __init__(self):
        self.sr_query_model = LLMModelAgent(SR_FILES_PATH,"t5-small",'sr_ind')
        self.doc_query_model = LLMModelAgent(DOC_FILES_PATH,"t5-small",'doc_ind')
        self.summarization_agent = SummarizationAgent("t5-small")
        self.modelState = ModelState()
        self.sr_citation_agent = SRCitationAgent()
        self.sr_citations={}
        self.doc_citation_agent = DocCitationAgent()
        self.doc_citations={}

        self.workflow_graph = langgraph.graph.StateGraph(dict)
        # Define and nodes to the workflow graph
        self.workflow_graph.add_node("START", self.no_operation)
        self.workflow_graph.add_node("sr_query_model", self.query_sr_model)
        self.workflow_graph.add_node("doc_query_model", self.query_doc_model)
        self.workflow_graph.add_node("summarization_model", self.query_summarization_model)

        # Define edges (connections) between nodes
        self.workflow_graph.add_edge(start_key="START", end_key="sr_query_model")
        # self.workflow_graph.add_edge(start_key="START", end_key="doc_query_model")
        self.workflow_graph.add_edge(start_key="sr_query_model", end_key="doc_query_model")
        # self.workflow_graph.add_edge(start_key="sr_query_model", end_key="summarization_model")
        self.workflow_graph.add_edge(start_key="doc_query_model", end_key="summarization_model")


        self.workflow_graph.set_entry_point("START")
        self.workflow_graph.set_finish_point("summarization_model")

        self.workflow_graph_compiled = self.workflow_graph.compile()


        from IPython.display import Image, display
        from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles
        image_data = self.workflow_graph_compiled.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API
        )
        # Save the image data to a file
        with open("workflow_graph.png", "wb") as f:
            f.write(image_data)

    #this stores the query state for the SR model
    def query_sr_model(self,state):
        sr_query = ""
        if "user_context" in state.keys():
            for user_context, sr_context in zip(state["user_context"], state["sr_context"]):
                sr_query = "\n".join(["User: "+user_context, "Response: "+sr_context])

        sr_query = "\n\n".join([sr_query, "Considering this context of previous chat history, answer this query in the context of Oracle Transport Management:: ", state["prompt"]])
        response = self.sr_query_model.generate_text(sr_query)
        self.sr_citations=self.sr_citation_agent.get_citation(response)
        state["sr_response"] = response.response
        return state

    #Stores the query state for the doc model
    def query_doc_model(self,state):
        doc_query=""
        if "user_context" in state.keys():
            for user_context, doc_context in zip(state["user_context"], state["doc_context"]):
                doc_query = "\n".join(["User: "+user_context, "Response: "+doc_context])
        doc_query = "\n".join([doc_query, "Considering this context of previous chat history, answer this query in the context of Oracle Transport Management: ", state["prompt"]])
        response = self.doc_query_model.generate_text(doc_query)
        self.doc_citations=self.doc_citation_agent.get_citation(response)
        state["doc_response"] = response.response
        return state

    #Stores the query state for the summarization model
    def query_summarization_model(self,state):
        summarization_query = "According to Support Request documents," + state["sr_response"] + ".\n\n According to OTM documentation, "+state["doc_response"] + ".\n\n Summarize both the responses."
        state["summary"]=self.summarization_agent.summarize_text(summarization_query)
        return state

    #When new chat is done no state needs to be stored
    def no_operation(self,state):
        return state

    #main function from where we run the model
    def run(self,user_input):
        self.modelState.state["prompt"] = user_input
        self.workflow_graph_compiled.invoke(self.modelState.state)
        self.modelState.update_contexts()
        #This is the model initializer agent which initializes the model
        return {
            "data":self.modelState.state["summary"],
            "sr_response":self.modelState.state["sr_response"],  
            "doc_response":self.modelState.state["doc_response"],
            "sr_citations":self.sr_citations,
            "doc_citations":self.doc_citations
        }    
    #flushes context, starts a new chat without any state
    def model_flush_context(self):
        self.modelState.flush_context()