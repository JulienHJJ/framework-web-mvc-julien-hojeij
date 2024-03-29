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
        # Récupérer les données du formulaire
        query = request.form['query']

        # Appeler la fonction pour récupérer le livre de l'API
        livre = get_livre_from_api(query)

        return render_template('recherche_livre.html', livre=livre)
    else:
        return render_template('recherche_livre.html', livre=None)


def get_livre_from_api(query):
    # Effectuer une requête à l'API de recherche de livres
    url = 'https://openlibrary.org/search.json'
    params = {'q': query}
    response = requests.get(url, params=params)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        # Analyser la réponse JSON
        data = response.json()
        if 'docs' in data and data['docs']:
            # Extraire les informations du premier livre trouvé
            premier_livre = data['docs'][0]
            titre = premier_livre.get('title', 'Titre inconnu')
            auteur = premier_livre.get('author_name', ['Auteur inconnu'])[0]
            couverture_id = premier_livre.get('cover_i')
            couverture_url = f'https://covers.openlibrary.org/b/id/{couverture_id}-L.jpg' if couverture_id else None

            # Récupérer d'autres informations si disponibles
            annee_publication = premier_livre.get('publish_year', ['Année de publication inconnue'])[0]
            num_pages = premier_livre.get('number_of_pages', 'Nombre de pages inconnu')
            isbn = premier_livre.get('isbn', ['ISBN inconnu'])[0]

            # Exemple: récupérer un genre aléatoire pour le livre (à modifier selon vos besoins)
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
        # En cas d'échec de la requête, retourner un message d'erreur
        return {"titre": "Erreur lors de la recherche", "auteur": "", "cover_url": None, "genre": "Genre inconnu"}



@app.route('/enregistrer_livre_api', methods=['POST'])
def enregistrer_livre_api():
    if request.method == 'POST':
        # Récupérer les détails du livre à partir de la requête
        titre = request.form['titre']
        auteur = request.form['auteur']
        genre_nom = request.form['genre']  # Récupérer le nom du genre du livre

        # Vérifier si le genre existe déjà dans la base de données
        genre = Genre.query.filter_by(nom=genre_nom).first()
        if not genre:
            # Si le genre n'existe pas, le créer et l'ajouter à la base de données
            genre = Genre(nom=genre_nom)
            db.session.add(genre)
            db.session.commit()

        # Enregistrer le livre dans la base de données en utilisant la fonction enregistrer_livre
        enregistrer_livre(titre, auteur, [genre_nom])

        # Redirection vers la page affichage_livres.html après l'enregistrement
        return redirect(url_for('affichage_livres'))
    else:
        # Ne pas effectuer de redirection si la méthode de requête n'est pas POST
        return render_template('accueil.html')  # Ou une autre page si nécessaire


from crud import *

if __name__ == '__main__':
    app.run(debug=True)