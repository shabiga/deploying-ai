import gradio as gr
import requests
from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from guardrails import block_topics

# setup small database for search
chroma_client = Client(Settings(persist_directory="./05_src/assignment_chat/chroma_db"))
embed_fn = embedding_functions.DefaultEmbeddingFunction()
collection = chroma_client.get_or_create_collection("info", embedding_function=embed_fn)

# load info file for search
try:
    with open("./05_src/assignment_chat/data/info.txt", "r") as f:
        data = f.readlines()
    collection.add(documents=data, ids=[str(i) for i in range(len(data))])
except:
    pass

# service 1: weather api
def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=j1"
        res = requests.get(url)
        info = res.json()
        temp = info["current_condition"][0]["temp_C"]
        desc = info["current_condition"][0]["weatherDesc"][0]["value"]
        return f"It’s {temp}°C in {city} with {desc.lower()}."
    except:
        return "Couldn’t get the weather right now."

# service 2: semantic search
def find_info(text):
    try:
        result = collection.query(query_texts=[text], n_results=2)
        if not result["documents"][0]:
            return "I didn’t find anything about that."
        out = " ".join(result["documents"][0])
        return f"Here’s something related: {out}"
    except:
        return "Something went wrong while searching."

# service 3: math function
def math_calc(expr):
    try:
        answer = eval(expr)
        return f"{expr} = {answer}"
    except:
        return "That’s not a valid math question."

# main chatbot
def chat_response(message, history):
    if block_topics(message):
        return "Sorry, I can’t talk about that."

    msg = message.lower()
    if "weather" in msg:
        if "in" in msg:
            city = msg.split("in")[-1].strip()
            return get_weather(city)
        else:
            return "Please say the city name."
    elif "search" in msg or "find" in msg:
        return find_info(message)
    elif any(op in msg for op in ["+", "-", "*", "/"]):
        return math_calc(message)
    else:
        return "Hi! I can tell the weather, search info, or do math. Try one!"

# gradio ui
with gr.Blocks() as demo:
    gr.Markdown("### 🤖 InfoBuddy Chatbot (Assignment 2)")
    chat = gr.Chatbot()
    text = gr.Textbox(placeholder="Type something here...")
    clear = gr.Button("Clear")

    def respond(msg, hist):
        reply = chat_response(msg, hist)
        hist.append((msg, reply))
        return "", hist

    text.submit(respond, [text, chat], [text, chat])
    clear.click(lambda: None, None, chat, queue=False)

if __name__ == "__main__":
    demo.launch(share=True)

