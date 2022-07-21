import os
from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.urandom(32)
    db.app = app
    db.init_app(app)
    db.create_all()


streaming_items = db.Table('streaming_items',
                           db.Column('streamingplatform_id', db.Integer, db.ForeignKey(
                               'streamingplatforms.id'), primary_key=True),
                           db.Column('movies_id', db.Integer, db.ForeignKey(
                               'movies.id'), primary_key=True)
                           )

'''
StreamingPlatform
Have name and movies
'''


class StreamingPlatform(db.Model):
    __tablename__ = 'streamingplatforms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    num_movies = db.Column(db.Integer, default=0)
    logo_url = db.Column(db.String(500))
    movies = db.relationship('Movie', secondary=streaming_items, backref=db.backref(
        'streamingplatforms', lazy=True))

    def __init__(self, name, num_movies, logo_url):
        self.name = name
        self.num_movies = num_movies
        self.logo_url = logo_url

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<StreamingPlatform ID: {self.id}, name: {self.name}>'

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'num_movies': self.num_movies,
            'logo_url': self.logo_url
        }


'''
Movie
Have title, release_date and director
'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    director = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.Date(), nullable=False)
    poster_url = db.Column(db.String(500))

    def __init__(self, title, director, release_date, poster_url):
        self.title = title
        self.director = director
        self.release_date = release_date
        self.poster_url = poster_url

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Movie ID: {self.id}, title: {self.title}, director: {self.director}, release_date: {self.release_date}>'

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'director': self.director,
            'release_date': self.release_date,
            'poster_url': self.poster_url
        }
