import sqlite3

def initialize_database(db_name='business.db'):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prix REAL NOT NULL
    )
    ''')
  

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fournisseur (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        adresse TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Livraison (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        prix TEXT NOT NULL
    )
    ''')
    
    

    conn.commit()
    conn.close()

    print("Database initialized, and tables are verified.")

# Only run if script is executed directly
if __name__ == '__main__':
    initialize_database()
