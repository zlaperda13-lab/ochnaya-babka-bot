import os
import random
import requests
from flask import Flask, request

app = Flask(__name__)

CONFIRMATION = os.environ.get("VK_CONFIRMATION", "")
SECRET = os.environ.get("VK_SECRET", "")
VK_TOKEN = os.environ.get("VK_TOKEN", "")
API_VERSION = "5.199"

STORIES = [
    "Говорят, в старом доме ночью иногда слышны шаги на втором этаже. Только второго этажа там нет.",
    "Один мужик каждую ночь видел в окне напротив силуэт человека. Однажды он понял, что смотрит в окно собственного дома.",
    "В лесу турист услышал, как кто-то позвал его по имени. Он пошёл на голос. Потом услышал тот же голос уже позади себя.",
]


def send_message(user_id, text):
    url = "https://api.vk.com/method/messages.send"

    params = {
        "access_token": VK_TOKEN,
        "v": API_VERSION,
        "user_id": user_id,
        "random_id": random.randint(1, 2147483647),
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
        text = message.get("text", "").strip().lower()

        if user_id:
            if text in ["помощь", "help", "меню"]:
                reply = (
                    "🦇 Ночная Бабка\n\n"
                    "Напиши:\n"
                    "«история» — получить страшную историю\n"
                    "«помощь» — показать это меню"
                )

            elif text in ["история", "страшилка", "страшная история"]:
                reply = "🌑 Вот тебе история...\n\n" + random.choice(STORIES)

            else:
                reply = (
                    "🦇 Ночная Бабка услышала тебя.\n\n"
                    "Напиши «история», если хочешь немного испортить себе сон."
                )

            send_message(user_id, reply)

    return "ok", 200


@app.route("/", methods=["GET"])
def home():
    return "Ночная Бабка работает"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
