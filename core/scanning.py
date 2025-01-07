import os
import json

from pathlib import Path

from settings import CASE_DIR


def get_statement_sum(folder_name: Path):
    filename = folder_name / 'statement_sum.json'

    with open(filename, 'r') as openfile:
        json_object = json.load(openfile)

    return json_object.get('sum')


def scan_folders():
    folders = os.listdir(CASE_DIR)

    for folder in folders:
        try:
            files = os.listdir(os.path.join(CASE_DIR, folder))
        except NotADirectoryError:
            continue

        if 'уведомление_об_отправке.pdf' in str(files):
            continue

        for file in files:
            if 'payment' in str(file):
                return folder


scan_folders()
