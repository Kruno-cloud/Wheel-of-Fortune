baza = 'BazaIgraca.db'
dokument = 'Kolo sreće PYTHON.txt'

import sqlite3

# Function to insert a category into the database and return its ID
def insert_category(cursor, category_name):
    cursor.execute("INSERT INTO Kategorije (Naziv) VALUES (?)", (category_name,))
    return cursor.lastrowid  # Get the ID of the last inserted row

# Function to insert a term and its description into the database
def insert_term(cursor, term_name, description, category_id):
    cursor.execute("INSERT INTO Pojmovi (Naziv, Opis, idKategorija) VALUES (?, ?, ?)", (term_name, description, category_id))

# Connect to the database
conn = sqlite3.connect(baza)
cursor = conn.cursor()

# Read and process the UTF-8 encoded TXT file with line breaks
with open(dokument, 'r', encoding='utf-8') as file:
    current_category_id = None
    current_category = None
    current_term_name = None
    current_description = None

    for line in file:
        line = line.strip()
        
        if line.startswith("Kategorija: "):
            current_category = line[len("Kategorija: "):]
            current_category_id = insert_category(cursor, current_category)
            print(f"Category: {current_category}")
        elif line.startswith("Pojam: "):
            current_term_name = line[len("Pojam: "):]
            print(f"Term Name: {current_term_name}")
        elif line.startswith("Opis: "):
            current_description = line[len("Opis: "):]
            if current_category_id is not None:
                insert_term(cursor, current_term_name, current_description, current_category_id)
                print(f"Description: {current_description}")

# Commit the changes and close the cursor and connection
conn.commit()
cursor.close()
conn.close()