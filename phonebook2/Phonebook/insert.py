import psycopg2
import csv
from config import load_config

def insert_by_csv(csv_file_path):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        name = row['name']
                        phone = row['phone']
                        cur.execute("""
                            INSERT INTO phonebook2 (name, phone) VALUES (%s, %s)
                        """, (name, phone))
        print("Succes!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
    

def insert_by_hand(name, phone):
    pp = load_config()
    try:
        with psycopg2.connect(**pp) as conn:
            with conn.cursor() as cur:
                cur.execute("""INSERT INTO PhoneBook (name, phone) VALUES (%s, %s)""", (name, phone))
        print("Succes!")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

print("Please choose one of two:\nC - CSV file\nH - Hand inserting")
type_insert = input()

if type_insert=='C':
    path = input('Please enter the path: ')
    insert_by_csv(path)
else:
    name, phone = input("Input user name: \n"), input("Input phone: ")
    insert_by_hand(name, phone)

    