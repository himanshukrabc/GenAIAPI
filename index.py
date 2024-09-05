from fastapi import FastAPI # type: ignore
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
import json
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

from model import Model
model=None
queries=""

@app.on_event("startup")
async def load_model():
    global model
    # Simulate model loading time
    model = Model()

# POST method to accept item data
@app.post("/")
async def query(item: Item):
    response = model.run(item.query)
    return response

# GET method to reset context
@app.post("/reset")
async def chat_reset_context():
    model.model_flush_context()
    return {"msg":"done"}

# Running the FastAPI application with Uvicorn (optional if running directly)
if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="127.0.0.1", port=8002)
