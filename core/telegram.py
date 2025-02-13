from datetime import datetime

import requests
from settings import TG_BOT_TOKEN


def get_updates():
    token = TG_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/getUpdates"

    response = requests.get(url)
    return response.json()


def prepare_message(statement_info: dict) -> str:
    message = f"""ИИН: {statement_info.get('iin')}
    ФИО: {statement_info.get('name')}
    ID ЗАЙМА: {statement_info.get('credit_id')}
    СУММА ИСКА: {statement_info.get('final_summa')}
    СУММА ГОСПОШЛИНЫ: {statement_info.get('state_duty')}
    УНИКАЛЬНЫЙ КОД ПЛАТЕЖА: <b>{statement_info.get('payment_code')}</b>
    ДАТА ЗАГРУЗКИ ИСКА: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
    """

    return message


def send_payment_info(statement_info: dict) -> str:
    message = prepare_message(statement_info)

    token = TG_BOT_TOKEN
    chat_ids = ["-4553001971", "-2227234613"]

    responses = []

    for chat_id in chat_ids:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        response = requests.get(
            url,
            params={
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'html'
            }
        )

        if response.status_code != 200:
            return f"Ошибка при отправке логов: {response.text}"

        responses.append({chat_id: response.text})
