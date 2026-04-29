import psycopg2
from config import load_config

def search(pattern):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                            SELECT id, name, phone
                            FROM phonebook2
                            WHERE name ILIKE %s OR phone ILIKE %s""" , (f"%{pattern}%", f"%{pattern}%"))
                result = cur.fetchall()
                if result:
                    for i in result:
                        print(f"ID: {i[0]}, Name: {i[1]}, Phone: {i[2]}")
                else:
                    print("No matches found.")
    except (psycopg2.DatabaseError, Exception) as error:
        print("Error:", error)
    
if __name__ == "__main__":
    pattern_input = input("Enter a name or phone pattern to search: ")
    search(pattern_input)