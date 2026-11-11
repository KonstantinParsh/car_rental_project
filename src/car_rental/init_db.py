import sqlite3
from pathlib import Path
from src.core.config import logger, DB_PATH, get_connection



def init_database(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = None

    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            reg_number TEXT NOT NULL UNIQUE
        );
        """)
        logger.info(
            "[УСПЕХ] Создана родительская таблица 'cars'."
        )

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            patronymic TEXT,
            license_number TEXT NOT NULL,
            phone TEXT NOT NULL,
            car_id INTEGER REFERENCES cars(id),
            rental_date TEXT NOT NULL
        );
        """)
        logger.info(
            "[УСПЕХ] Создана дочерняя таблица 'clients'"
        )

        conn.commit()
        print("База данных и таблицы успешно инициализированы.")

    except sqlite3.Error as e:
        print(f"Произошла ошибка при работе с SQLite: {e}")
        logger.error(
            f"[ОШИБКА] {e}"
        )
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()


def main() -> None:
    init_database(DB_PATH)


if __name__ == "__main__":
    main()