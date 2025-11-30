import psycopg2
from config import load_config

def insert_or_update_user(name, phone):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
            
                cur.execute("SELECT * FROM phonebook2 WHERE name = %s", (name,))
                existing_user = cur.fetchone()

                if existing_user:
                  
                    cur.execute("UPDATE phonebook2 SET phone = %s WHERE name = %s", (phone, name))
                    print(f" Updated phone number for '{name}'.")
                else:
                   
                    cur.execute("INSERT INTO phonebook2 (name, phone) VALUES (%s, %s)", (name, phone))
                    print(f" Inserted new user: {name}.")
    except (psycopg2.DatabaseError, Exception) as error:
        print("❌ Error:", error)

if __name__ == "__main__":
    name = input(" name: ")
    phone = input(" phone : ")
    insert_or_update_user(name, phone)
