import os
from flask import Flask, render_template, request, jsonify
from groq import Groq
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

history = []
system_prompt = "You are a helpful AI assistant. Keep answers short and direct."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global history
    
    data = request.json
    user_message = data["message"]
    
    history.append({"role": "user", "content": user_message})
    
    if len(history) > 10:
        history = history[-10:]
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt}
            ] + history
        )
        
        ai_reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": ai_reply})
        
        return jsonify({"reply": ai_reply, "status": "success"})
    
    except Exception as e:
        return jsonify({"reply": f"Error: {e}", "status": "error"})

if __name__ == "__main__":
    app.run(debug=True)
