import sqlite3

def get_table_names(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
    tables = cursor.fetchall()
    return [table[0] for table in tables]


def get_columns_for_table(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    return [(column[1], column[2]) for column in columns]  # [(nom_colonne, type_colonne), ...]

def create_class_code(table_name, columns):
    class_code = f"class {table_name.capitalize()}:\n"
    class_code += "    def __init__(self, " + ", ".join([f"{col[0]}=None" for col in columns]) + "):\n"
    
    # Constructeur
    for col in columns:
        class_code += f"        self.{col[0]} = {col[0]}\n"
    
    # Getters et Setters
    for col in columns:
        # Getter
        class_code += f"\n    def get_{col[0]}(self):\n"
        class_code += f"        return self.{col[0]}\n"
        
        # Setter
        class_code += f"\n    def set_{col[0]}(self, value):\n"
        class_code += f"        self.{col[0]} = value\n"
    
    return class_code

def generate_classes_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Récupérer toutes les tables
    tables = get_table_names(cursor)
    
    all_classes_code = ""
    
    for table in tables:
        columns = get_columns_for_table(cursor, table)
        class_code = create_class_code(table, columns)
        all_classes_code += class_code + "\n\n"  # Ajouter chaque classe générée
        
    conn.close()
    
    return all_classes_code

db_path = 'db1.db'

classes_code = generate_classes_from_db(db_path)


with open('Generated Classes.py', 'w') as f:
    f.write(classes_code) 
