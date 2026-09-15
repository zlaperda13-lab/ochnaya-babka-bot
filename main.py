import os
import requests
from flask import Flask, request

app = Flask(__name__)

CONFIRMATION = os.environ.get("VK_CONFIRMATION", "")
SECRET = os.environ.get("VK_SECRET", "")
VK_TOKEN = os.environ.get("VK_TOKEN", "")
API_VERSION = "5.199"


def send_message(user_id, text):
    url = "https://api.vk.com/method/messages.send"

    params = {
        "access_token": VK_TOKEN,
        "v": API_VERSION,
        "user_id": user_id,
        "random_id": 0,
        "message": text,
    }

    response = requests.post(url, params=params, timeout=10)
    return response.json()


@app.route("/callback", methods=["GET", "POST"])
def callback():
    data = request.get_json(silent=True) or {}

    if data.get("type") == "confirmation":
        return CONFIRMATION, 200

    if SECRET and data.get("secret") != SECRET:
        return "invalid secret", 403

    if data.get("type") == "message_new":
        message = data.get("object", {}).get("message", {})

        user_id = message.get("from_id")
        text = message.get("text", "").strip()

        if user_id and text:
            send_message(
                user_id,
                "Ночная Бабка услышала тебя. 🦇\n\n"
                f"Ты написал: {text}"
            )

    return "ok", 200


@app.route("/", methods=["GET"])
def home():
    return "Ночная Бабка работает"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
