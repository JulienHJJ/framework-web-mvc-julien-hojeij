from flask_sqlalchemy import SQLAlchemy
from database import db

class Livre(db.Model):
    __tablename__ = 'livre'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(50))
    genres = db.relationship('Livre_Genre', back_populates='livre')

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    livres = db.relationship('Livre_Genre', back_populates='genre')

class Livre_Genre(db.Model):
    __tablename__ = 'livre_genre'
    livre_id = db.Column(db.Integer, db.ForeignKey('livre.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)
    livre = db.relationship("Livre", back_populates='genres')
    genre = db.relationship("Genre", back_populates='livres')