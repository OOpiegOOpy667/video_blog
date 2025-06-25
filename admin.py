from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "videoblogsecretkey123"  # Clé secrète pour les sessions

# Configuration de la base de données
DB_PATH = 'videoblog.db'

# Fonction pour obtenir une connexion à la base de données
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Fonction pour initialiser la base de données
def init_db():
    # Vérifier si la base de données existe déjà
    db_exists = os.path.exists(DB_PATH)
    
    # Créer une connexion à la base de données
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Créer la table admin si elle n'existe pas, en lisant les fichiers SQL schema.sql et initialisation_db.sql
    if not db_exists:
        with open('schema.sql', 'r') as f:
            cursor.executescript(f.read())
        
        with open('initialisation_db.sql', 'r') as f:
            cursor.executescript(f.read())
    
    conn.commit()
    conn.close()

# Initialiser la base de données au démarrage
init_db()

@app.route('/')
def index():
    return render_template('index.html')

# Route principale pour la page admin
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    error = None
    
    if request.method == 'POST':
        password = request.form.get('password')
        
        # Vérifier si le mot de passe existe dans la table admin
        conn = get_db_connection()
        cursor = conn.cursor()
        admin_users = cursor.execute('SELECT password FROM admin').fetchall()
        conn.close()
        
        # Vérifier si le mot de passe soumis correspond à l'un des mots de passe dans la base
        if any(password == row['password'] for row in admin_users):
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            error = "Mot de passe incorrect"
    
    return render_template('admin.html', error=error)

# Route de déconnexion
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)