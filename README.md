💬 AI Chatbot with Gradio UI & Hugging Face

Dự án này là một ứng dụng Chatbot hoàn chỉnh với giao diện Web trực quan, được xây dựng bằng Gradio và sử dụng mô hình Llama 3.3 thông qua Groq API. Đây là dự án kết thúc lộ trình học tập để trở thành AI Engineer, tập trung vào khả năng triển khai ứng dụng thực tế trên môi trường đám mây.

🔗 Live Demo

Trải nghiệm trực tiếp ứng dụng tại: https://huvimal-ai-chatbot.hf.space

🌟 Tính năng nổi bật
Giao diện Web mượt mà: Sử dụng Gradio Blocks để tạo trải nghiệm trò chuyện hiện đại và trực quan.

Đa dạng nhân vật (Multi-Personas): Người dùng có thể chuyển đổi giữa các vai trò như "Trợ lý thông thường", "Code Mentor", hoặc "Gia sư".

Streaming Response: Hiển thị câu trả lời theo thời gian thực, mang lại cảm giác tương tác tự nhiên và nhanh chóng.

Tùy chỉnh linh hoạt: Tích hợp thanh trượt Temperature để người dùng điều chỉnh mức độ sáng tạo của câu trả lời.

📁 Cấu trúc dự án
app.py: Mã nguồn chính xử lý logic hội thoại, tích hợp Groq API và xây dựng giao diện Gradio.

requirements.txt: Danh sách các thư viện cần thiết để triển khai dự án (gradio, groq, python-dotenv).

.gitignore: Đã cấu hình để bảo vệ thông tin nhạy cảm và tệp tin rác.

🚀 Hướng dẫn cài đặt
1. Clone repository
git clone https://github.com/huvimal/AI-Chatbot-Gradio.git
cd AI-Chatbot-Gradio
2. Thiết lập API Key
Tạo file .env và thêm mã API Groq của bạn:

GROQ_API_KEY=your_api_key_here
3. Cài đặt và Chạy
python -m venv .venv
# Active venv (Windows: .\.venv\Scripts\activate | Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
python app.py

🛠 Công nghệ sử dụng

Frontend: Gradio UI.

Model: Llama-3.3-70b-versatile (via Groq Cloud).

Deployment: Hugging Face Spaces.

Backend: Python, Dotenv.

👤 Tác giả
Lê Mai Vĩnh Hưng 
Lĩnh vực quan tâm: AI Engineering, Data Engineering, Blockchain.
