import sqlite3
from pathlib import Path
from src.core.config import DB_PATH, get_connection



def selector(db_path: Path) -> None:
    conn = None
    try:
        conn = get_connection(db_path)
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys;")
        row = cursor.fetchone()
        keys_check = bool(row[0])
        print(f"Внешние ключи включены: {keys_check}")

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        table_names = [row[0] for row in tables]
        print("Таблицы:", ", ".join(table_names))
        for name in table_names:
            cursor.execute(f"PRAGMA table_info({name});")
            columns = cursor.fetchall()

            print(f"\nТаблица {name}:")
            for cid, col_name, col_type, notnull, default, pk in columns:
                print(f"    {cid}: {col_name} {col_type}, NOT_NULL={bool(notnull)}, PK={bool(pk)}")

        cursor.execute("PRAGMA foreign_key_list(clietns);")
        for fk in cursor.fetchall():
            print(f"    {fk[3]} -> {fk[2]}.{fk[4]}")

        conn.commit()

    except sqlite3.Error as e:
        print(f"Произошла ошибка при работе с SQLite: {e}")
        if conn:
            conn.rollback()

    finally:
        if conn:
            conn.close()


def main() -> None:
    selector(DB_PATH)


if __name__ == "__main__":
    main()