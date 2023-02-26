from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# film and genre table
film_genre = db.Table('film_genre',
                      db.Column('id_film', db.Integer, db.ForeignKey('film.id')),
                      db.Column('id_genre', db.Integer, db.ForeignKey('genre.id'))
                      )


# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    about_me = db.Column(db.String(250))
    password_hash = db.Column(db.String(128))
    id_film_watched = db.Column(db.Integer, db.ForeignKey('film.id'))
    confirm = db.Column(db.Boolean)

    def __repr__(self):
        return f'{self.username}'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Film model
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    type = db.Column(db.String(32))
    duration = db.Column(db.Integer)
    year = db.Column(db.Integer)
    country = db.Column(db.String(32))
    id_director = db.Column(db.Integer, db.ForeignKey('director.id'))
    film_watched = db.relationship('User', backref='film')
    genres = db.relationship('Genre', secondary=film_genre, backref='films')

    def __repr__(self):
        return f'{self.name}'


# Genre model
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False, unique=True)

    def __repr__(self):
        return f'{self.name}'


# Director model
class Director(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    films = db.relationship('Film', backref='director')

    def __repr__(self):
        return f'{self.name}'


# User loader
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
