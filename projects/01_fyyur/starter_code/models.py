from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link= db.Column(db.String(120))
    seeking_talent= db.Column(db.Boolean)
    seeking_description=db.Column(db.String(500))
    shows = db.relationship('Show', backref="venue", lazy=True)


    @property
    def search(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    # TODO: implement any missing fields, as a database migration using Flask-Migrate DONE

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String()))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link= db.Column(db.String(120))
    seeking_venue= db.Column(db.Boolean)
    seeking_description=db.Column(db.String(500))
    shows = db.relationship('Show', backref="artist", lazy=True) 
 
    
    @property
    def search(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    # TODO: implement any missing fields, as a database migration using Flask-Migrate DONE

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__='shows'

  id= db.Column(db.Integer, primary_key=True)
  artist_id= db.Column(db.Integer, db.ForeignKey('artists.id') ,nullable=False)
  venue_id= db.Column(db.Integer,db.ForeignKey('venues.id'), nullable=False)
  start_time= db.Column(db.DateTime, nullable=False)
  venue_deletion = db.relationship('Venue', backref=db.backref('shows_venue', cascade='all, delete'))


