import psycopg2
from config import load_config

def delete_user(name, phone):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL delete_user(%s::TEXT, %s::TEXT)", (name, phone))
        print("User deleted successfully (if existed).")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Error:", error)


if __name__ == "__main__":
    name_input = input("Enter name to delete (or leave empty): ").strip() or None
    phone_input = input("Enter phone to delete (or leave empty): ").strip() or None
    delete_user(name_input, phone_input)
