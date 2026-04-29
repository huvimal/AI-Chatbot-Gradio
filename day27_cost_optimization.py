from groq import Groq
from dotenv import load_dotenv
import hashlib, json, time
from pathlib import Path

load_dotenv()
client = Groq()

# ── Simple cache để tránh gọi API lặp lại ────────────────
CACHE_FILE = "response_cache.json"

def load_cache():
    if Path(CACHE_FILE).exists():
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def get_cache_key(prompt: str, model: str) -> str:
    return hashlib.md5(f"{model}:{prompt}".encode()).hexdigest()

cache = load_cache()

def cached_ask(prompt: str, max_tokens: int = 300) -> dict:
    key = get_cache_key(prompt, "qwen/qwen3-32b")

    # Cache hit — không gọi API
    if key in cache:
        print(f"  [CACHE HIT] Tiết kiệm ~{cache[key]['tokens']} tokens")
        return {"reply": cache[key]["reply"], "tokens": 0, "cached": True}

    # Cache miss — gọi API
    start = time.time()
    r = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        temperature=0
    )
    elapsed = time.time() - start
    reply = r.choices[0].message.content
    tokens = r.usage.total_tokens

    # Lưu vào cache
    cache[key] = {"reply": reply, "tokens": tokens}
    save_cache(cache)
    print(f"  [API CALL] {tokens} tokens, {elapsed:.2f}s")
    return {"reply": reply, "tokens": tokens, "cached": False}

# Test cache
questions = [
    "RAG là gì?",
    "Vector database dùng để làm gì?",
    "RAG là gì?",  # câu hỏi lặp lại — sẽ dùng cache
    "Vector database dùng để làm gì?",  # lặp lại
]

total_saved = 0
for q in questions:
    print(f"Hỏi: {q}")
    result = cached_ask(q)
    print(f"Trả lời: {result['reply'][:80]}...")
    if result["cached"]:
        total_saved += cache[get_cache_key(q, "qwen/qwen3-32b")]["tokens"]

print(f"Tổng token tiết kiệm nhờ cache: {total_saved}")