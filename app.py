from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resoruces={r"/*": {"origins": [
    "http://localhost:8888",
    "https://your-site.netlify.app"
]
}})

@app.route("/health", methods=["GET"])
def health():
    return {"ok": True}

@app.route("/contact", methods=["POST"])
def contact():
    """
    Expected JSON body:
    {
        "name": "Jane",
        "email": "jane@example.com"
        "message": "hello"
    }
    """

    data=request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email","").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({ok: False, "error": "Missing required fields"}), 400

    print(f"[CONTACT] {name} <{email}>: {message[:120]}")


    return jsonify({"ok": True, "msg": "Thanks, we'll be in touch!"})