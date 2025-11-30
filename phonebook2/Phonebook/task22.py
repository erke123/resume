import psycopg2
from config import load_config

def insert_or_update_user(name, phone):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL insert_or_update_user(%s::TEXT, %s::TEXT)", (name, phone))
        print("successfully (if existed).")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Error:", error)


if __name__ == "__main__":
    name_input = input("Enter name  ").strip() or None
    phone_input = input("Enter phone  ").strip() or None
    insert_or_update_user(name_input, phone_input)
