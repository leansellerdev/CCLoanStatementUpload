import os
import json

from pathlib import Path

from settings import CASE_DIR


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

        return folder
