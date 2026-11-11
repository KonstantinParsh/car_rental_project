import sqlite3
from pathlib import Path
from src.core.config import DB_PATH, get_connection



def integrity_check(db_path: Path) -> None:
    conn = None

    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO clients (first_name, last_name, license_number, phone, car_id, rental_date) VALUES (?, ?, ?, ?, ?, ?)",
            ("Тест", "Тестов", "23451235", "79233421032", 9999, "2026-12-20")
        )
        conn.commit()
        print("Запись вставлена - внешний ключ НЕ работает.")

    except sqlite3.IntegrityError as e:
        print(f"Ошибка целостности - внешний ключ работает корректно ({e}).")
        conn.rollback()

    finally:
        if conn:
            conn.close()


def main() -> None:
    integrity_check(DB_PATH)


if __name__ == "__main__":
    main()