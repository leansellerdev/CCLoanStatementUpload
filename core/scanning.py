import os
import json
from datetime import datetime

from pathlib import Path

from settings import CASE_DIR, RESULTS_DIR


def get_statement_info(folder_name: Path) -> dict:
    filename = folder_name / 'statement_info.json'

    with open(filename, 'r', encoding='utf-8') as openfile:
        json_object = json.load(openfile)

    return json_object


def scan_folders() -> str:
    folders = os.listdir(CASE_DIR)

    for folder in folders:
        try:
            files = os.listdir(os.path.join(CASE_DIR, folder))
        except NotADirectoryError:
            continue

        if 'уведомление_об_отправке.pdf' in str(files):
            continue

        if '_ПлатежПор.pdf' in str(files):
            return folder


def get_total_todays_cases() -> int:
    folders = os.listdir(RESULTS_DIR)

    paths = [os.path.join(RESULTS_DIR, basename) for basename in folders]
    all_cases_times = [
        datetime.fromtimestamp(os.path.getmtime(file)).strftime('%d:%m:%Y') for file in paths
    ]

    todays_cases_times_with_payment = [
        time for time in all_cases_times if datetime.today().strftime('%d:%m:%Y') == time
    ]

    return len(todays_cases_times_with_payment)


# def get_total_todays_cases_with_payment() -> int:
#     folders = os.listdir(RESULTS_DIR)
#     paths = []
#
#     for folder in folders:
#         for filename in os.listdir(os.path.join(RESULTS_DIR, folder)):
#             if filename.endswith('_ПлатежПор.pdf'):
#                 paths.append(os.path.join(RESULTS_DIR, folder))
#
#     all_cases_times = [
#         datetime.fromtimestamp(os.path.getmtime(file)).strftime('%d:%m:%Y') for file in paths
#     ]
#
#     todays_cases_times_with_payment = [
#         time for time in all_cases_times if datetime.today().strftime('%d:%m:%Y') == time
#     ]
#
#     return len(todays_cases_times_with_payment)
#
#
# def get_total_todays_cases_without_payment() -> int:
#     folders = os.listdir(RESULTS_DIR)
#     paths = []
#
#     for folder in folders:
#         for filename in os.listdir(os.path.join(RESULTS_DIR, folder)):
#             if filename.endswith('_ПлатежПор.pdf'):
#                 break
#             paths.append(os.path.join(RESULTS_DIR, folder))
#
#     all_cases_times = [
#         datetime.fromtimestamp(os.path.getmtime(file)).strftime('%d:%m:%Y') for file in paths
#     ]
#
#     todays_cases_times_without_payment = [
#         time for time in all_cases_times if datetime.today().strftime('%d:%m:%Y') == time
#     ]
#
#     return len(todays_cases_times_without_payment)
