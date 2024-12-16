import sqlite3


class Client:
    def __init__(self, id, nom, prenom): #constructeur
        self.id = id
        self.nom = nom
        self.prenom = prenom
    
    def __repr__(self): #toString
        return f"Client(id={self.id}, nom='{self.nom}', prenom='{self.prenom}')"

class Produit:
    def __init__(self, id, nom, prix):  # constructeur
        self.id = id
        self.nom = nom
        self.prix = prix
    
    def __repr__(self):  # toString
        return f"Produit(id={self.id}, nom='{self.nom}', prix={self.prix})"

#def get_all_clients_from_db():
 #   my_db = 'db1.db'
  #  conn = sqlite3.connect(my_db)
   # cursor = conn.cursor()
    #cursor.execute("SELECT * FROM client")
    #rows = cursor.fetchall()

    #clients_list = []
    
    #for row in rows:
     #   id, nom, prenom = row
      #  client = Client(id, nom, prenom)
       # clients_list.append(client)

    #conn.close()
    
    #return clients_list

def get_all_from_db(table_name, cls):
    my_db = 'db1.db'
    conn = sqlite3.connect(my_db)
    cursor = conn.cursor()

    
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    rows = cursor.fetchall()

    # Récupération des noms de colonnes 
    column_names = [description[0] for description in cursor.description]
    
    # Création de la liste d'objets
    objects_list = []
    
    for row in rows:
        # Génération dynamique d'objets avec les attributs correspondants
        attributes = {column_names[i]: row[i] for i in range(len(row))}
        obj = cls(**attributes)  # Création de l'objet en passant les attributs dynamiquement
        objects_list.append(obj)

    conn.close()
    
    return objects_list
# Test
#It Allows You to Execute Code When the File Runs as a Script,
#but Not When It's Imported as a Module

if __name__ == '__main__': 
    produits = get_all_from_db('produit', Produit)
    
    for p in produits:
        print(p)

     
    
