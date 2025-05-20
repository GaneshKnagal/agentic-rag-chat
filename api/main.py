from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from agent.llm_agent import agent_chat
from pydantic import BaseModel


app = FastAPI()

# Enable CORS so frontend (HTML/JS) can access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the input schema for POST /chat
class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat(data: ChatRequest):
    query = data.query.strip()

    if not query:
        return {"error": "Query cannot be empty"}

    try:
        response = await agent_chat(query)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}

# Optional: run via `python api/main.py`
if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)

