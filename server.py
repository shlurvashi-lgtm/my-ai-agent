from flask import Flask, request, jsonify
import urllib.request, json, os, datetime

app = Flask(__name__)
API_KEY = os.environ.get("OPENROUTER_KEY", "")
HISTORY_FILE = "chat_history.json"

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    return response

@app.route("/ask", methods=["POST", "OPTIONS"])
def ask():
    if request.method == "OPTIONS":
        return jsonify({}), 200

    question = request.json["question"]
    data = json.dumps({
        "model": "openrouter/free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for Swami Construction. Help visitors with questions about construction services, projects and quotes."},
            {"role": "user", "content": question}
        ]
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=data,
        headers={"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"}
    )
    result = json.loads(urllib.request.urlopen(req).read())
    answer = result["choices"][0]["message"]["content"]

    # Save to history
    entry = {
        "time": datetime.datetime.now().isoformat(),
        "question": question,
        "answer": answer
    }
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            history = json.load(f)
    history.append(entry)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    return jsonify({"answer": answer})

@app.route("/history")
def history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            return jsonify(json.load(f))
    return jsonify([])

@app.route("/")
def home():
    return "AI Agent is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
