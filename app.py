from flask import Flask, render_template, request, redirect, url_for
from database import db
import os
import requests

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def accueil():
    return render_template('accueil.html')


@app.route('/affichage_livres', methods=['GET','POST'])
def affichage_livres():
    livres = Livre.query.all()
    genres = Genre.query.all()
    return render_template('affichage_livres.html', livres=livres, genres=genres)


@app.route('/recherche_livre', methods=['GET', 'POST'])
def recherche_livre():
    if request.method == 'POST':
        query = request.form['query']

        livre = get_livre_from_api(query)

        return render_template('recherche_livre.html', livre=livre)
    else:
        return render_template('recherche_livre.html', livre=None)


def get_livre_from_api(query):
    url = 'https://openlibrary.org/search.json'
    params = {'q': query}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'docs' in data and data['docs']:
            premier_livre = data['docs'][0]
            titre = premier_livre.get('title', 'Titre inconnu')
            auteur = premier_livre.get('author_name', ['Auteur inconnu'])[0]
            couverture_id = premier_livre.get('cover_i')
            couverture_url = f'https://covers.openlibrary.org/b/id/{couverture_id}-L.jpg' if couverture_id else None

            annee_publication = premier_livre.get('publish_year', ['Année de publication inconnue'])[0]
            num_pages = premier_livre.get('number_of_pages', 'Nombre de pages inconnu')
            isbn = premier_livre.get('isbn', ['ISBN inconnu'])[0]
            genre = Genre.query.first()

            return {
                "titre": titre,
                "auteur": auteur,
                "cover_url": couverture_url,
                "publish_year": annee_publication,
                "num_pages": num_pages,
                "isbn": isbn,
                "genre": genre.nom if genre else "Genre inconnu"
            }
        else:
            return {"titre": "Aucun livre trouvé", "auteur": "", "cover_url": None, "genre": "Genre inconnu"}
    else:
        return {"titre": "Erreur lors de la recherche", "auteur": "", "cover_url": None, "genre": "Genre inconnu"}



@app.route('/enregistrer_livre_api', methods=['POST'])
def enregistrer_livre_api():
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        genre_nom = request.form['genre']

        genre = Genre.query.filter_by(nom=genre_nom).first()
        if not genre:
            genre = Genre(nom=genre_nom)
            db.session.add(genre)
            db.session.commit()

        enregistrer_livre(titre, auteur, [genre_nom])

        return redirect(url_for('affichage_livres'))
    else:
        return render_template('accueil.html')


from crud import *

if __name__ == '__main__':
    app.run(debug=True)