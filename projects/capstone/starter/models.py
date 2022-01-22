from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String,Date
from flask_migrate import Migrate
import os


DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
DB_NAME = os.getenv('DB_NAME', 'capstone')
database_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)




class Movie(db.Model):
    __tablename__='movies'
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(String,nullable=False)
    release_date=db.Column(Date,nullable=False)
    actors = db.relationship ('Actor', backref="movie", lazy=True)

    def update(self):

        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short(self):
        return { "id": self.id, "title": self.title, "release_date": self.release_date}


class Actor(db.Model):

    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String,nullable=False)
    age = db.Column(Integer,nullable=False)
    gender = db.Column(String,nullable=False)
    movies_id= db.Column(db.Integer, db.ForeignKey('movies.id'))
 

    def update(self):

        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def short (self):
        return { "id": self.id, "name": self.name, "age": self.age, "gender": self.gender, "movies_id":self.movies_id}
