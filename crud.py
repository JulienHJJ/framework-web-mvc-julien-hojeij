from flask import render_template, request, redirect
from database import db
from app import app
from livre import Livre
from livre import Genre


def enregistrer_livre(titre, auteur, genres):
    genres_objets = []
    for genre_nom in genres:
        genre = Genre.query.filter_by(nom=genre_nom).first()
        if not genre:
            genre = Genre(nom=genre_nom)
            db.session.add(genre)
        genres_objets.append(genre)

    livre = Livre(titre=titre, auteur=auteur, genres=genres_objets)
    db.session.add(livre)
    db.session.commit()
    return redirect("/affichage_livres")

@app.route('/ajouter', methods=['POST'])
def ajouter_livre():
    titre = request.form['titre']
    auteur = request.form['auteur']
    genre_id = request.form['genre_id']
    nouveau_livre = Livre(titre=titre, auteur=auteur)
    db.session.add(nouveau_livre)

    genre = Genre.query.get(genre_id)
    if genre:
        nouveau_livre.genres.append(genre)
    db.session.commit()
    livres = Livre.query.all()
    genres = Genre.query.all()

    return render_template('affichage_livres.html', livres=livres, genres=genres)


@app.route('/modifier/<int:id>', methods=['POST'])
def modifier_livre(id):
    livre = Livre.query.get_or_404(id)
    nouveau_titre = request.form['nouveau_titre']
    nouveau_auteur = request.form['nouveau_auteur']
    livre.titre = nouveau_titre
    livre.auteur = nouveau_auteur
    db.session.commit()
    print(Livre.query.all())
    return redirect("/affichage_livres")

@app.route('/supprimer/<int:id>', methods=['POST'])
def supprimer_livre(id):
    livre = Livre.query.get_or_404(id)
    db.session.delete(livre)
    db.session.commit()
    return redirect("/affichage_livres")

@app.route('/ajouter_genre', methods=['POST'])
def ajouter_genre():
    nom = request.form['nom']
    nouveau_genre = Genre(nom=nom)
    db.session.add(nouveau_genre)
    db.session.commit()
    livres = Livre.query.filter(Livre.genres.any(Genre.id == nouveau_genre.id)).all()
    genres = Genre.query.all()

    return render_template('affichage_livres.html', livres=livres, genres=genres)

@app.route('/modifier_genre/<int:id>', methods=['POST'])
def modifier_genre(id):
    genre = Genre.query.get_or_404(id)
    nouveau_nom = request.form['nouveau_nom']
    genre.nom = nouveau_nom
    db.session.commit()
    return redirect("/affichage_livres")

@app.route('/supprimer_genre/<int:id>', methods=['POST'])
def supprimer_genre(id):
    genre = Genre.query.get_or_404(id)
    db.session.delete(genre)
    db.session.commit()
    return redirect("/affichage_livres")