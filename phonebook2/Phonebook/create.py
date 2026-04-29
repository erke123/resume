import psycopg2
from config import load_config

def create_phonebook_table():
    command = """
    CREATE TABLE IF NOT EXISTS phonebook2 (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        phone VARCHAR(50) NOT NULL
    )
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
                print("Таблица phonebook2 создана.")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Ошибка при создании таблицы:", error)

if __name__ == '__main__':
    create_phonebook_table()
