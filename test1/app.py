from flask import Flask, render_template, request, jsonify
import sqlite3
from createDb import initialize_database  # Import the database initialization function

app = Flask(__name__)

my_bd = 'business.db'

# Initialize database tables on every access of index route
@app.before_request
def before_request():
    """Verify or create tables in the database before handling requests."""
    initialize_database(my_bd)

def get_table_names():
    """Récupère tous les noms de tables de la base de données spécifiée."""
    conn = sqlite3.connect(my_bd)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def get_table_data_and_structure(table_name):
    """Récupère les colonnes et les données d'une table spécifique de la base de données."""
    conn = sqlite3.connect(my_bd)
    cursor = conn.cursor()
    
    # Obtenir les colonnes de la table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    
    # Obtenir toutes les données de la table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    conn.close()
    return columns, rows

@app.route('/tables')
def tables():
    """Renvoie la liste de toutes les tables de la base de données."""
    tables = get_table_names()
    return jsonify(tables)

@app.route('/table_data', methods=['POST'])
def table_data():
    """Renvoie les colonnes et les données d'une table sélectionnée."""
    table_name = request.json.get('table_name')
    columns, rows = get_table_data_and_structure(table_name)
    return jsonify({"columns": columns, "data": rows})

@app.route('/add_row', methods=['POST'])
def add_row():
    """Ajoute une nouvelle entrée dans la table spécifiée."""
    table_name = request.json.get('table_name')
    data = request.json.get('data')  # Les données à insérer (clé:valeur)

    conn = sqlite3.connect(my_bd)
    cursor = conn.cursor()
    
    # Prépare la requête d'insertion dynamique
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?"] * len(data))
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor.execute(query, list(data.values()))
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": f"Row added to {table_name} successfully"}), 201

@app.route('/delete_row', methods=['DELETE'])
def delete_row():
    """Supprime une entrée d'une table spécifique en fonction de son ID."""
    table_name = request.json.get('table_name')
    primary_key = request.json.get('primary_key')  # Valeur de l'identifiant de la ligne

    conn = sqlite3.connect(my_bd)
    cursor = conn.cursor()
    
    # Supposons que le premier champ soit la clé primaire
    cursor.execute(f"PRAGMA table_info({table_name})")
    primary_column = cursor.fetchone()[1]
    
    # Supprime la ligne correspondante
    query = f"DELETE FROM {table_name} WHERE {primary_column} = ?"
    cursor.execute(query, (primary_key,))
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": f"Row deleted from {table_name} successfully"}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
