# 📰 NewsChat – Chat with the Latest News in Sri Lanka  

NewsChat is a **conversational news assistant** that allows users to chat with the latest Sri Lankan news instead of scrolling through endless headlines.  
It combines **web scraping, NLP, embeddings, vector search, and LLMs** to deliver contextual answers in a simple chat interface.  

---

🔎 Built with:
- Web Scraping (requests + BeautifulSoup) for fresh news
- NLP Preprocessing (NLTK) for tokenization, stopword removal, and lemmatization
- Semantic Embeddings & Retrieval (SentenceTransformers + FAISS)
- Conversational AI powered by Groq + LLaMA 3.1-8B-Instant  

---

## 🛠️ Tech Stack  
- **Python**  
- **Flask** – Web framework  
- **BeautifulSoup + Requests** – Web scraping  
- **NLTK** – Text preprocessing  
- **SentenceTransformers (all-MiniLM-L6-v2)** – Embeddings  
- **FAISS** – Vector similarity search  
- **Groq API (LLaMA 3.1-8B-Instant)** – Conversational AI  

---

## 📂 Project Structure  
```
NewsChat/
│── app.py               
│── main_functions.py             
│── templates/           
│   └── index.html       
│── Dockerfile           
│── gunicorn.conf.py
│── requirements.txt    
│── README.md             
```

---

## ⚡ Installation & Setup without docker image

 Clone the repository:  
```bash
git clone https://github.com/JPasindu/NewsChat.git
cd NewsChat
```

 Create a virtual environment:  
```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

 Install dependencies:  
```bash
pip install -r requirements.txt
```

 Set up your **Groq API key**:  
```bash
export GROQ_API_KEY="your_api_key_here"   # Linux/Mac
set GROQ_API_KEY="your_api_key_here"      # Windows
```

Run the app:  
```bash
python app.py
```

Open in browser:
```
http://127.0.0.1:5000/
```

---

## 🎯 Usage  
- Enter a question like:  
  - *“What’s the latest political update in Sri Lanka?”*  
  - *“Summarize today’s top news.”*  

---

## 📸 Screenshot  
<img width="1434" height="816" alt="Screenshot 2025-09-02 at 12 58 12" src="https://github.com/user-attachments/assets/194ea8fa-2a22-4930-b8b9-738aad987b4a" />
<img width="1434" height="816" alt="Screenshot 2025-09-02 at 12 59 32" src="https://github.com/user-attachments/assets/e636f7f5-bacc-4e58-9fd3-77fb3b687863" />
<img width="1434" height="816" alt="Screenshot 2025-09-02 at 13 00 51" src="https://github.com/user-attachments/assets/45d52d19-f81d-4237-8a17-90dce039f8bd" />
<img width="1434" height="816" alt="Screenshot 2025-09-02 at 13 02 35" src="https://github.com/user-attachments/assets/cdad0dc4-30c2-4bd2-8c0e-b32099f0adcb" />

---
