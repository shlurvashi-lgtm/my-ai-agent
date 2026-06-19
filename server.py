from flask import Flask, request, jsonify
import urllib.request, json, os

app = Flask(__name__)
API_KEY = os.environ.get("OPENROUTER_KEY", "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")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json["question"]
    data = json.dumps({
        "model": "openrouter/free",
        "messages": [{"role": "user", "content": question}]
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=data,
        headers={"Authorization": "Bearer " + API_KEY, "Content-Type": "application/json"}
    )
    result = json.loads(urllib.request.urlopen(req).read())
    answer = result["choices"][0]["message"]["content"]
    return jsonify({"answer": answer})

@app.route("/")
def home():
    return "AI Agent is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)