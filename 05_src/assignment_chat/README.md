# Assignment 2 – Conversational AI Chatbot

### About
This is my chatbot called **InfoBuddy**.  
It can do 3 main things:
1. Tell the weather using an API  
2. Search short facts from a small text file  
3. Solve math problems  

It’s made with **Gradio**, **ChromaDB**, and **Python**.

---

### Services
**Service 1:** Weather API (wttr.in)  
**Service 2:** Semantic search using ChromaDB  
**Service 3:** Simple calculator  

---

### Guardrails
It won’t talk about:
- cats or dogs  
- horoscopes or zodiac  
- Taylor Swift  

---

### Personality
InfoBuddy talks in a short and casual way.

---

### How to Run
1. Open the folder in VS Code  
2. In the terminal run:  

pip install gradio chromadb requests  
python 05_src/assignment_chat/app.py
