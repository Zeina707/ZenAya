from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, send_file
from flask_bcrypt import Bcrypt
from user_dao import UserDAO
import os
import zipfile
import io
import shutil
import json
import re

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
    return render_template('customize2.html', template_id=2, template_path='views/template2/index.html')

@app.route('/customize/template3')
def customize_template3():
    return render_template('customize3.html', template_id=3, template_path='views/template3/index.html')

# Générer et télécharger le ZIP du template personnalisé
@app.route('/generate-zip', methods=['POST'])
def generate_zip():
    template_id = request.form.get('template_id')
    removed_elements = request.form.getlist('removed_elements')
    
    # Get custom styles from the form
    customization_data = {}
    for key in request.form:
        if key.startswith('customization'):
            # Extract the customization data using regex
            match = re.search(r'customization\[(.*?)\](?:\[(.*?)\])?(?:\[(.*?)\])?', key)
            if match:
                parts = [p for p in match.groups() if p is not None]
                if len(parts) == 1:
                    # Simple key like customization[removed][]
                    if parts[0] not in customization_data:
                        customization_data[parts[0]] = [request.form[key]]
                    else:
                        customization_data[parts[0]].append(request.form[key])
                elif len(parts) >= 2:
                    # Nested key like customization[colors][primary]
                    if parts[0] not in customization_data:
                        customization_data[parts[0]] = {}
                    
                    if len(parts) == 2:
                        customization_data[parts[0]][parts[1]] = request.form[key]
                    elif len(parts) == 3:
                        if parts[1] not in customization_data[parts[0]]:
                            customization_data[parts[0]][parts[1]] = {}
                        customization_data[parts[0]][parts[1]][parts[2]] = request.form[key]
    
    # Create a ZIP file in memory
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add template files to the ZIP
        template_dir = os.path.join(app.root_path, 'templates', 'views', f'template{template_id}')
        static_dir = os.path.join(app.root_path, 'static')
        
        # Read the main HTML file
        main_html_path = os.path.join(template_dir, 'index.html')
        with open(main_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply customizations to HTML content
        # 1. Handle removed elements
        if 'removed' in customization_data:
            for element_id in customization_data['removed']:
                # Hide elements with matching ID
                content = content.replace(f'id="{element_id}"', f'id="{element_id}" style="display:none;"')
        
        # 2. Handle modified elements
        if 'modified' in customization_data:
            for element_id, modifications in customization_data['modified'].items():
                # Create a pattern to find the element with its ID
                pattern = f'<([a-zA-Z0-9]+)([^>]*?)id="{element_id}"([^>]*?)>(.*?)</\\1>'
                
                def replace_element(match):
                    tag, attrs1, attrs2, content = match.groups()
                    
                    # Apply text modifications if provided
                    new_content = modifications.get('text', content)
                    
                    # Apply style modifications if provided
                    style_attr = f' style="{modifications.get("style", "")}"'
                    
                    return f'<{tag}{attrs1}id="{element_id}"{attrs2}{style_attr}>{new_content}</{tag}>'
                
                # Use re.sub with a callback function
                content = re.sub(pattern, replace_element, content, flags=re.DOTALL)
        
        # Generate custom CSS to apply colors and fonts
        custom_css = ""
        
        # 3. Handle colors
        if 'colors' in customization_data:
            colors = customization_data['colors']
            if 'primary' in colors:
                custom_css += f"""
                .btn-primary, .primary-color, .navbar, .bg-primary {{
                    background-color: {colors['primary']} !important;
                    border-color: {colors['primary']} !important;
                }}
                .text-primary {{
                    color: {colors['primary']} !important;
                }}
                """
            
            if 'secondary' in colors:
                custom_css += f"""
                .btn-secondary, .secondary-color, .bg-secondary {{
                    background-color: {colors['secondary']} !important;
                    border-color: {colors['secondary']} !important;
                }}
                .text-secondary {{
                    color: {colors['secondary']} !important;
                }}
                """
            
            if 'background' in colors:
                custom_css += f"""
                body {{
                    background-color: {colors['background']} !important;
                }}
                .bg-light, .bg-white {{
                    background-color: {colors['background']} !important;
                }}
                """
        
        # 4. Handle fonts
        if 'fonts' in customization_data:
            fonts = customization_data['fonts']
            if 'heading' in fonts:
                custom_css += f"""
                h1, h2, h3, h4, h5, h6, .h1, .h2, .h3, .h4, .h5, .h6 {{
                    font-family: {fonts['heading']} !important;
                }}
                """
            
            if 'body' in fonts:
                custom_css += f"""
                body, p, div, span, a, input, button, textarea, select, .body-text {{
                    font-family: {fonts['body']} !important;
                }}
                """
            
            if 'headingSize' in fonts:
                custom_css += f"""
                h1, .h1 {{ font-size: {fonts['headingSize']} !important; }}
                h2, .h2 {{ font-size: calc({fonts['headingSize']} * 0.8) !important; }}
                h3, .h3 {{ font-size: calc({fonts['headingSize']} * 0.7) !important; }}
                h4, .h4 {{ font-size: calc({fonts['headingSize']} * 0.6) !important; }}
                """
            
            if 'bodySize' in fonts:
                custom_css += f"""
                body, p, .body-text {{
                    font-size: {fonts['bodySize']} !important;
                }}
                """
        
        # Add a custom CSS file to the ZIP
        if custom_css:
            zf.writestr('css/custom-styles.css', custom_css)
            
            # Add a link to the custom CSS in the HTML
            if '<head>' in content:
                head_end = content.find('</head>')
                if head_end != -1:
                    custom_css_link = '<link rel="stylesheet" href="css/custom-styles.css">'
                    content = content[:head_end] + custom_css_link + content[head_end:]
        
        # Write the modified HTML to the ZIP
        zf.writestr('index.html', content)
        
        # Add all other files from the template directory (CSS, JS, images, etc.)
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if file != 'index.html':  # We've already processed this file
                    file_path = os.path.join(root, file)
                    # Determine the relative path in the ZIP
                    arcname = os.path.relpath(file_path, template_dir)
                    zf.write(file_path, arcname)
        
        # Add static assets if they exist
        if os.path.exists(static_dir):
            for root, dirs, files in os.walk(static_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Determine the relative path in the ZIP
                    rel_path = os.path.relpath(file_path, static_dir)
                    zf.write(file_path, os.path.join('static', rel_path))
    
    # Reset the file pointer and send the ZIP
    memory_file.seek(0)
    return send_file(memory_file, download_name=f'template{template_id}_personalisé.zip', as_attachment=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = UserDAO.get_user_by_email(email)
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])  # Convertir l'ObjectId en chaîne
            flash('Connexion réussie !', 'success')
            return redirect(url_for('index'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')
    return render_template('login.html')



@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    UserDAO.create_user(name, email, hashed_password)
    flash('Compte créé avec succès ! Connectez-vous maintenant.', 'success')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
    


