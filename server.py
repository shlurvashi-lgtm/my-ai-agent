from flask import Flask, request, jsonify
import urllib.request, json, os

app = Flask(__name__)

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
    API_KEY = "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"
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
    return jsonify({"answer": result["choices"][0]["message"]["content"]})

@app.route("/")
def home():
    return "AI Agent is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
