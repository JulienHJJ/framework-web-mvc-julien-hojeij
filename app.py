from flask import Flask, render_template, request, redirect
from crud import LivreRepository

app = Flask(__name__)
repo_livre = LivreRepository()

@app.route('/')
def index():
    return render_template('affichage_livres.html', livres=repo_livre.lire_tous())

@app.route('/ajouter', methods=['POST'])
def ajouter_livre():
    titre = request.form['titre']
    auteur = request.form['auteur']
    repo_livre.creer(titre, auteur)  # Utilisation de repo_livre pour créer un nouveau livre
    return render_template('affichage_livres.html', livres=repo_livre.lire_tous())

@app.route('/modifier/<int:id>', methods=['POST'])
def modifier_livre(id):
    nouveau_titre = request.form['nouveau_titre']
    nouveau_auteur = request.form['nouveau_auteur']
    livre = repo_livre.lire_par_id(id)
    if nouveau_titre:
        livre.titre = nouveau_titre
    if nouveau_auteur:
        livre.auteur = nouveau_auteur
    return redirect('/')

@app.route('/supprimer/<int:id>', methods=['POST'])
def supprimer_livre(id):
    repo_livre.supprimer(id)
    return redirect('/')


if __name__ == '__main__':
    app.run()
