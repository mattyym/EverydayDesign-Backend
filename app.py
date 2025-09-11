import os, requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": [
    "http://localhost:8888",
    "https://interiordesignwebpage.netlify.app"
]
}})

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
FROM_EMAIL = os.environ.get("FROM_EMAIL")
TO_EMAIL = os.environ.get("TO_EMAIL")

@app.route("/health", methods=["GET"])
def health():
    return {"ok": True}


def send_email(name: str, phone: str, email: str, message: str) -> bool:
    if not (RESEND_API_KEY and FROM_EMAIL and TO_EMAIL):
        print("[MAIL] Missing RESEND_API_KEY / FROM_EMAIL / TO_EMAIL")
        return False

    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "from": FROM_EMAIL,      
        "to": [TO_EMAIL],         
        "reply_to": email,
        "subject": f"New contact from {name}",
        "text": f"Name: {name}\nEmail: {email}\n Phone: {phone}\n\nMessage:\n{message}"
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"[RESEND] status={r.status_code} body={r.text[:300]}")
        return r.ok
    except Exception as e:
        print("[RESEND][ERROR]", e)
        return False

@app.route("/contact", methods=["POST"])
def contact():
    """
    Expected JSON body:
    {
        "name": "Jane",
        "email": "jane@example.com"
        "phone" :"1234567890"
        "message": "hello"
    }
    """

    data=request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email","").strip()
    phone = data.get("phone", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not phone or not message:
        return jsonify({"ok": False, "error": "Missing required fields"}), 400

    print(f"[CONTACT] {name} {phone} <{email}>: {message[:120]}")

    _ = send_email(name, phone, email, message)


    return jsonify({"ok": True, "msg": "Thanks, we'll be in touch!"})