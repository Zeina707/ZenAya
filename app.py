from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
from flask_bcrypt import Bcrypt
from DAO.user_dao import UserDAO
import os

# Initialisation de l'application Flask
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'votre_cle_secrete'

# Définir le chemin vers la racine du projet
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Page principale (accueil)
@app.route('/')
@app.route('/')
def index():
    return render_template('pages/index.html')  # Charger la page d'accueil



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
