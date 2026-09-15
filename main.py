import os
from flask import Flask, request

app = Flask(__name__)

CONFIRMATION = os.environ.get("VK_CONFIRMATION", "")
SECRET = os.environ.get("VK_SECRET", "")

@app.route("/callback", methods=["GET", "POST"])
def callback():
    data = request.get_json(silent=True) or {}

    if data.get("type") == "confirmation":
        return CONFIRMATION, 200

    if SECRET and data.get("secret") != SECRET:
        return "invalid secret", 403

    return "ok", 200

@app.route("/", methods=["GET"])
def home():
    return "Ночная Бабка работает"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
