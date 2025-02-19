from datetime import datetime

import requests
from settings import TG_BOT_TOKEN, LOG_FILE_PATH, PROJECT_NAME

LOGS_CHAT_ID = '-4751461230'
PAYMENTS_CHAT_ID = '-4553001971'


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


def send_logs(log_file: str = LOG_FILE_PATH, message: str = 'log'):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendDocument"

    message = f'Процесс: {PROJECT_NAME}\n' + message

    with open(log_file, 'rb') as send_file:
        response = requests.post(
            url,
            data={
                'chat_id': LOGS_CHAT_ID,
                'caption': message,
            },
            files={
                'document': send_file,
            }
        )

    return response


def send_payment_info(statement_info: dict) -> str:
    message = prepare_message(statement_info)

    responses = []

    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    response = requests.get(
        url,
        params={
            'chat_id': PAYMENTS_CHAT_ID,
            'text': message,
            'parse_mode': 'html'
        }
    )

    if response.status_code != 200:
        return f"Ошибка при отправке логов: {response.text}"

    responses.append({PAYMENTS_CHAT_ID: response.text})


if __name__ == '__main__':
    updates = send_logs()
    print(updates.text)
