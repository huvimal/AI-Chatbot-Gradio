import gradio as gr
from groq import Groq
from dotenv import load_dotenv
import os

# Khởi tạo API
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PERSONAS = {
    "Trợ lý thông thường": "Bạn là trợ lý AI thân thiện, trả lời bằng tiếng Việt.",
    "Code Mentor": "Bạn là senior developer, giải thích code rõ ràng bằng tiếng Việt.",
    "Gia sư": "Bạn là gia sư kiên nhẫn, giải thích từng bước bằng tiếng Việt.",
}

def chat(message, history, persona_name, temperature):
    """
    Hàm xử lý thông minh: 
    Tự động chuyển đổi giữa List và Dict để 'chiều' mọi phiên bản Gradio.
    """
    system_prompt = PERSONAS.get(persona_name, PERSONAS["Trợ lý thông thường"])
    
    # 1. Chuyển đổi history sang dạng tin nhắn cho Groq
    messages = [{"role": "system", "content": system_prompt}]
    
    for item in history:
        # Nếu history là dạng dict (bản mới)
        if isinstance(item, dict):
            messages.append(item)
        # Nếu history là dạng list/tuple [user, bot] (bản cũ)
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            u, a = item
            if u: messages.append({"role": "user", "content": u})
            if a: messages.append({"role": "assistant", "content": a})
    
    messages.append({"role": "user", "content": message})

    try:
        response_stream = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=temperature,
            max_tokens=1000,
            stream=True
        )

        # 2. Xây dựng history mới theo dạng DICTIONARY (Vì log yêu cầu dict)
        updated_history = list(history)
        updated_history.append({"role": "user", "content": message})
        updated_history.append({"role": "assistant", "content": ""})

        reply = ""
        for chunk in response_stream:
            if chunk.choices[0].delta.content:
                reply += chunk.choices[0].delta.content
                # Cập nhật nội dung tin nhắn cuối
                updated_history[-1] = {"role": "assistant", "content": reply}
                yield updated_history
                
    except Exception as e:
        yield history + [{"role": "user", "content": message}, {"role": "assistant", "content": f"Lỗi: {str(e)}"}]

# ── Giao diện ──────────────────────────────────────────────────────────────
with gr.Blocks(title="AI Chatbot — Project") as demo:
    gr.Markdown("# AI Chatbot Xây dựng bởi Vĩnh Hưng")

    with gr.Row():
        with gr.Column(scale=1):
            persona = gr.Dropdown(
                choices=list(PERSONAS.keys()),
                value="Trợ lý thông thường",
                label="Chọn Persona"
            )
            temperature = gr.Slider(0, 1, value=0.7, step=0.1, label="Temperature")
            
        with gr.Column(scale=3):
            # QUAN TRỌNG: KHÔNG để type="messages" để tránh lỗi TypeError
            # Nhưng hàm chat() ở trên vẫn trả về Dict để tránh lỗi Data Incompatible
            chatbot = gr.Chatbot(height=450, label="Hội thoại")
            msg = gr.Textbox(placeholder="Nhập tin nhắn...", label="Tin nhắn")

            with gr.Row():
                send_btn = gr.Button("Gửi", variant="primary")
                clear_btn = gr.Button("Xóa lịch sử")

    # Sự kiện
    send_btn.click(chat, [msg, chatbot, persona, temperature], chatbot).then(lambda: "", None, [msg])
    msg.submit(chat, [msg, chatbot, persona, temperature], chatbot).then(lambda: "", None, [msg])
    clear_btn.click(lambda: [], None, chatbot)

if __name__ == "__main__":
    # Loại bỏ theme khỏi Blocks và chạy thẳng launch
    demo.launch()