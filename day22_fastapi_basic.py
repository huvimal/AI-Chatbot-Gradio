from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import uvicorn

load_dotenv()
client = Groq()
app = FastAPI(title="AI Chat API", version="1.0")

# Request/Response schema
class ChatRequest(BaseModel):
    message: str
    system_prompt: str = "Bạn là trợ lý AI thân thiện, trả lời bằng tiếng Việt."
    temperature: float = 0.7
    max_tokens: int = 500

class ChatResponse(BaseModel):
    reply: str
    input_tokens: int
    output_tokens: int

@app.get("/")
def root():
    return {"message": "AI Chat API đang chạy!", "docs": "/docs"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        r = client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=[
                {"role": "system", "content": req.system_prompt},
                {"role": "user", "content": req.message}
            ],
            temperature=req.temperature,
            max_tokens=req.max_tokens
        )
        return ChatResponse(
            reply=r.choices[0].message.content,
            input_tokens=r.usage.prompt_tokens,
            output_tokens=r.usage.completion_tokens
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)