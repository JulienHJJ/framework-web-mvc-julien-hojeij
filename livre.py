from database import db

livre_genre = db.Table('livre_genre',
    db.Column('livre_id', db.Integer, db.ForeignKey('livre.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

class Livre(db.Model):
    __tablename__ = 'livre'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(50))
    auteur = db.Column(db.String(100))
    genres = db.relationship('Genre', secondary=livre_genre, back_populates='livres')

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    livres = db.relationship('Livre', secondary=livre_genre, back_populates='genres')