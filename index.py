from fastapi import FastAPI # type: ignore
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json
app = FastAPI()

# Allow CORS for specific origins
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Data model for incoming request
class Item(BaseModel):
    query: str

from model import SRTModel
from model2 import LangChain
model=None

@app.on_event("startup")
async def load_model():
    global model
    # Simulate model loading time
    model = LangChain("t5-small", "t5-small")
    # model = SRTModel()

# POST method to accept item data
@app.post("/")
async def query(item: Item):
    return model.run(item.query)

# Running the FastAPI application with Uvicorn (optional if running directly)
if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="0.0.0.0", port=8000)
