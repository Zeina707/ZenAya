import sqlite3
my_db = 'db1.db'
def ajouter_client(nom, prenom):
    insertion = "INSERT INTO client (nom, prenom) VALUES (?, ?)"
    cursor.execute(insertion, (nom, prenom))
    conn.commit()

def ajouter_produit(nom, prix):
    insertion = "INSERT INTO produit (nom, prix) VALUES (?, ?)"
    cursor.execute(insertion, (nom, prix))
    conn.commit()

table_client = '''
                    CREATE TABLE IF NOT EXISTS client(
                        id integer primary key AUTOINCREMENT, 
                        nom TEXT NOT NULL,
                        prenom TEXT NOT NULL)
                    '''
table_produit = '''
                    CREATE TABLE IF NOT EXISTS produit(
                        id integer primary key AUTOINCREMENT, 
                        nom TEXT NOT NULL,
                        prix REAL NOT NULL)
                '''

conn = sqlite3.connect(my_db)

cursor = conn.cursor()
cursor.execute(table_client)
cursor.execute(table_produit)
ajouter_produit('Chaise', 49.99)
ajouter_produit('Table', 129.99)
ajouter_produit('Lampe', 25.50)
ajouter_client('Mokrini', 'Zeina')
ajouter_client('Mokrini', 'Leila')

conn.commit()


conn.close()