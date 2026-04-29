from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq()

def ask(prompt, system="Bạn là trợ lý hữu ích.", temp=0.7):
    r = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        temperature=temp,
        max_tokens=500
    )
    return r.choices[0].message.content

def llm_judge(question: str, answer: str, criteria: list) -> dict:
    """Dùng LLM để đánh giá chất lượng câu trả lời."""
    criteria_str = "".join([f"- {c}" for c in criteria])
    prompt = f"""Đánh giá câu trả lời sau theo các tiêu chí bên dưới.
Trả về JSON với format: {{"scores": {{"criterion": score}}, "overall": score, "feedback": "nhận xét"}}
Score từ 1-10. Chỉ trả về JSON, không giải thích thêm.

Câu hỏi: {question}
Câu trả lời: {answer}

Tiêu chí đánh giá:
{criteria_str}"""

    result = ask(prompt, temp=0)
    try:
        # Tìm JSON trong response
        import re
        match = re.search(r'{{.*}}', result, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return {"error": "Không parse được JSON", "raw": result}

# Test suite
test_cases = [
    {
        "question": "Python là gì?",
        "answer": ask("Python là gì?")
    },
    {
        "question": "RAG là gì?",
        "answer": ask("RAG là gì?")
    },
    {
        "question": "Giải thích neural network",
        "answer": ask("Giải thích neural network")
    }
]

criteria = [
    "Độ chính xác: thông tin có đúng không?",
    "Độ rõ ràng: có dễ hiểu không?",
    "Độ đầy đủ: có bao quát đủ không?",
    "Ngôn ngữ: tiếng Việt có tự nhiên không?"
]

print("=== KẾT QUẢ ĐÁNH GIÁ ===")
total_score = 0
for i, tc in enumerate(test_cases):
    print(f"Test {i+1}: {tc['question']}")
    print(f"Trả lời: {tc['answer'][:100]}...")
    result = llm_judge(tc["question"], tc["answer"], criteria)
    if "overall" in result:
        score = result["overall"]
        total_score += score
        print(f"Điểm tổng: {score}/10")
        print(f"Nhận xét: {result.get('feedback', 'N/A')}")
    print("-" * 40)

print(f"Điểm trung bình: {total_score/len(test_cases):.1f}/10")