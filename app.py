from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, send_file
from flask_bcrypt import Bcrypt
from DAO.user_dao import UserDAO
import os
import zipfile
import io
import shutil

# Initialisation de l'application Flask
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'votre_cle_secrete'

# Définir le chemin vers la racine du projet
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Page principale (accueil)
@app.route('/')
def index():
    return render_template('pages/index.html')  # Charger la page d'accueil

# Appeler l'index dans le template1 2 3 same as previous stuff
@app.route('/template1')
def index_template1():
    return render_template('views/template1/index.html')  # acceuil template 1

@app.route('/template2')
def index_template2():
    return render_template('views/template2/index.html')  # acceuil template 2

@app.route('/template3')
def index_template3():
    return render_template('views/template3/index.html')  # acceuil template 3

# Routes pour customiser les templates
@app.route('/customize/template1')
def customize_template1():
    return render_template('customize.html', template_id=1, template_path='views/template1/index.html')

@app.route('/customize/template2')
def customize_template2():
    return render_template('customize.html', template_id=2, template_path='views/template2/index.html')

@app.route('/customize/template3')
def customize_template3():
    return render_template('customize.html', template_id=3, template_path='views/template3/index.html')

# Générer et télécharger le ZIP du template personnalisé
@app.route('/generate-zip', methods=['POST'])
def generate_zip():
    template_id = request.form.get('template_id')
    removed_elements = request.form.getlist('removed_elements')
    
    # Créer un fichier ZIP en mémoire
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Ajouter les fichiers du template au ZIP
        template_dir = os.path.join(app.root_path, 'templates', 'views', f'template{template_id}')
        
        # Lire le fichier HTML principal
        main_html_path = os.path.join(template_dir, 'index.html')
        with open(main_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Modifier le contenu pour masquer les éléments sélectionnés
        for element_id in removed_elements:
            # Cette méthode simple recherche les balises avec l'ID spécifié
            # et ajoute style="display:none;" pour les masquer
            content = content.replace(f'id="{element_id}"', f'id="{element_id}" style="display:none;"')
        
        # Ajouter le fichier HTML modifié au ZIP
        zf.writestr('index.html', content)
        
        # Ajouter tous les autres fichiers du template (assets, CSS, JS, etc.)
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if file != 'index.html':  # On a déjà traité ce fichier
                    file_path = os.path.join(root, file)
                    # Déterminer le chemin relatif dans le ZIP
                    arcname = os.path.relpath(file_path, template_dir)
                    zf.write(file_path, arcname)
        
        # Ajouter les assets statiques communs si nécessaire
        static_dir = os.path.join(app.root_path, 'static')
        if os.path.exists(static_dir):
            for root, dirs, files in os.walk(static_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Déterminer le chemin relatif dans le ZIP
                    arcname = os.path.join('static', os.path.relpath(file_path, static_dir))
                    zf.write(file_path, arcname)
    
    # Réinitialiser le pointeur du fichier et renvoyer le ZIP
    memory_file.seek(0)
    return send_file(memory_file, download_name=f'template{template_id}_personalisé.zip', as_attachment=True)

# Route d'inscription
@app.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    if not name or not email or not password:
        flash('Tous les champs sont requis', 'error')
        return redirect(url_for('login'))
    user_dao = UserDAO()
    if user_dao.get_user_by_email(email):
        flash('Cet email est déjà utilisé', 'error')
        return redirect(url_for('login'))
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user_dao.create_user(name, email, hashed_password)
    flash('Compte créé avec succès ! Connectez-vous.', 'success')
    return redirect(url_for('login'))

# Route de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    login_path = os.path.join(app.root_path, 'templates', 'login.html')
    if not os.path.exists(login_path):
        return f"Le fichier login.html est introuvable à l'emplacement {login_path}"
   
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_dao = UserDAO()
        user = user_dao.authenticate_user(email, password)
        if user:
            session['user_id'] = str(user['_id'])
            session['user_name'] = user['name']
            flash('Connexion réussie !', 'success')
            return redirect(url_for('index'))  # Rediriger vers la page d'accueil
        else:
            flash('Email ou mot de passe incorrect', 'error')
    return render_template('login.html')  # Afficher le formulaire de login

# Route de déconnexion
@app.route('/logout')
def logout():
    session.clear()
    flash('Vous êtes déconnecté', 'success')
    return redirect(url_for('login'))  # Rediriger vers la page de login après la déconnexion

if __name__ == '__main__':
    app.run(debug=True)