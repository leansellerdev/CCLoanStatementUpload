import requests
from settings import TG_BOT_TOKEN


def get_uodates():
    token = TG_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/getUpdates"

    response = requests.get(url)
    return response.json()


def send_logs(message, log_file=None):
    token = TG_BOT_TOKEN
    chat_ids = ["-4553001971", "-2227234613"]

    responses = []

    for chat_id in chat_ids:
        if log_file:
            url = f"https://api.telegram.org/bot{token}/sendDocument"
            with open(log_file, "rb") as sendfile:
                response = requests.post(
                    url,
                    data={
                        "chat_id": chat_id,
                        "caption": message
                    },
                    files={"document": sendfile}
                )
        else:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            response = requests.get(
                url,
                params={'chat_id': chat_id, 'text': message}
            )

        if response.status_code != 200:
            return f"Ошибка при отправке логов: {response.text}"

        responses.append({chat_id: response.text})

    return response.text