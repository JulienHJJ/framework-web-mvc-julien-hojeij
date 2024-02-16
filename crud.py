from flask import render_template, request, redirect
from app import app, db
from livre import Livre

@app.route('/ajouter', methods=['POST'])
def ajouter_livre():
    titre = request.form['titre']
    auteur = request.form['auteur']
    nouveau_livre = Livre(titre=titre, auteur=auteur)
    db.session.add(nouveau_livre)
    db.session.commit()
    return redirect('/')


@app.route('/modifier/<int:id>', methods=['POST'])
def modifier_livre(id):
    livre = Livre.query.get_or_404(id)
    nouveau_titre = request.form['nouveau_titre']
    nouveau_auteur = request.form['nouveau_auteur']
    livre.titre = nouveau_titre
    livre.auteur = nouveau_auteur
    db.session.commit()
    return redirect('/')

@app.route('/supprimer/<int:id>', methods=['POST'])
def supprimer_livre(id):
    livre = Livre.query.get_or_404(id)
    db.session.delete(livre)
    db.session.commit()
    return redirect('/')