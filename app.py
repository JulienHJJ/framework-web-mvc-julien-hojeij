from flask import Flask
from database import db
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/')
def affichage_livres():
    livres = Livre.query.all()
    genres = Genre.query.all()
    return render_template('affichage_livres.html', livres=livres, genres=genres)

from crud import *

if __name__ == '__main__':
    app.run(debug=True)