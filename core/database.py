import sqlite3
from datetime import datetime

from settings import DB_PATH


class SQLiteDatabse:
    def __init__(self, file_name: str = DB_PATH) -> None:
        self.file_name = file_name
        self.conn = sqlite3.connect(file_name, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def add_case(self, iin, credit_id, payment_sum, payment_code, court_name) -> None:
        create_date = datetime.now()

        self.cursor.execute(
            """
            INSERT INTO cases (iin, credit_id, payment_sum, payment_code, court_name, create_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (iin, credit_id, payment_sum, payment_code, court_name, create_date)
        )

        self.conn.commit()
