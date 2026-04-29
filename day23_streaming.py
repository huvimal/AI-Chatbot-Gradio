from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import uvicorn, json

load_dotenv()
client = Groq()
app = FastAPI(title="Streaming AI API")

class ChatRequest(BaseModel):
    message: str
    system_prompt: str = "Bạn là trợ lý AI, trả lời bằng tiếng Việt."

def generate_stream(message: str, system: str):
    """Generator stream từng token từ LLM."""
    stream = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": message}
        ],
        stream=True,  # BẬT streaming
        max_tokens=500
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            # Gửi từng token dạng Server-Sent Events
            data = json.dumps({"token": delta.content})
            yield f"data: {data}"
    yield "data: [DONE]"

@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    return StreamingResponse(
        generate_stream(req.message, req.system_prompt),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )

@app.get("/")
def root():
    return {"message": "Streaming API ready", "endpoint": "/chat/stream"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)