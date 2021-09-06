#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import sys 
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm as Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database DONE
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

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


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  regions= Venue.query.distinct(Venue.city, Venue.state).all()
  data=[]
  for region in regions:

    tmp_venues=[]
    venues= Venue.query.filter_by(state=region.state).filter_by(city=region.city).all()
    for venue in venues:
      tmp_venues.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": len(db.session.query(Show).filter(Show.start_time>datetime.now()).all())

      })

    data.append({
      "city": region.city,
      "state": region.state,
      "venues": tmp_venues
 
    })


       


  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search=request.form.get('search_term', '')
  venues=Venue.query.filter(Venue.name.ilike("%"+ search + "%")).all()
  data=[]
  for venue in venues:
    data.append(venue.search)
    response={ 
      "count": len(venues),
      "data": data
    }
 
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id
  venue_btn= db.session.query(Venue).get(venue_id) #for all Venue data

  upcoming=db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time>=datetime.now()).all()
  upcoming_shows=[]
  for event in upcoming:

    upcoming_shows.append({
      "artist_id": event.artist_id,
      "artist_name": event.artist.name,
      "artist_image_link": event.artist.image_link,
      "start_time": event.start_time.strftime('%Y-%m-%d %H:%M:%S')

    })

  past=db.session.query(Show).join(Venue).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()
  past_shows=[]
  for event in past:

    past_shows.append({
      "artist_id": event.artist_id,
      "artist_name": event.artist.name,
      "artist_image_link": event.artist.image_link,
      "start_time": event.start_time.strftime('%Y-%m-%d %H:%M:%S')

    })
  data={
    "id": venue_btn.id,
    "name": venue_btn.name,
    "genres": venue_btn.genres,
    "address": venue_btn.address,
    "city": venue_btn.city,
    "state": venue_btn.state,
    "phone": venue_btn.phone,
    "website": venue_btn.website_link,
    "facebook_link": venue_btn.facebook_link,
    "seeking_talent": venue_btn.seeking_talent,
    "seeking_description": venue_btn.seeking_description,
    "image_link": venue_btn.image_link,
    "upcoming_shows": upcoming_shows,
    "past_shows": past_shows,
    "upcoming_shows_count": len(upcoming_shows),
    "past_shows_count": len(past_shows)

  }
  

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  form = VenueForm(request.form)
  # TODO: modify data to be the data object returned from db insertion
  try:
    new_venue = Venue(
      name=form.name.data,
      city=form.city.data,
      state=form.state.data,
      address=form.address.data,
      phone=form.phone.data,
      genres=form.genres.data,
      image_link=form.image_link.data,
      facebook_link=form.facebook_link.data,
      website_link=form.website_link.data,
      seeking_talent=form.seeking_talent.data,
      seeking_description=form.seeking_description.data)
    db.session.add(new_venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
     # TODO: on unsuccessful db insert, flash an error instead. 
     # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
     # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
   flash( 'An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
   print(sys.exc_info())
   db.session.rollback()
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database
  data= Artist.query.all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search=request.form.get('search_term', '')
  artists=Artist.query.filter(Artist.name.ilike("%"+ search + "%")).all()
  data=[]
  for artist in artists:
    data.append(artist.search)

    response={
      "count": len(artists),
      "data": data
    }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # DONE: replace with real artist data from the artist table, using artist_id
  upcoming=db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show.start_time>=datetime.now()).all()
  upcoming_shows=[]
  for event in upcoming:
    upcoming_shows.append({
      "venue_id": event.venue_id,
      "venue_name": event.venue.name,
      "venue_image_link": event.venue.image_link,
      "start_time": event.start_time.strftime('%Y-%m-%d %H:%M:%S')

    })
  past=db.session.query(Show).join(Artist).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all()
  past_shows=[]
  for event in past:
    past_shows.append({
      "venue_id": event.venue_id,
      "venue_name": event.venue.name,
      "venue_image_link": event.venue.image_link,
      "start_time": event.start_time.strftime('%Y-%m-%d %H:%M:%S')   
    })
  artist_btn= db.session.query(Artist).get(artist_id)
  data={
    "id": artist_btn.id,
    "name": artist_btn.name,
    "genres": artist_btn.genres,
    "city": artist_btn.city,
    "state": artist_btn.state,
    "phone": artist_btn.phone,
    "website": artist_btn.website_link,
    "facebook_link": artist_btn.facebook_link,
    "seeking_venue": artist_btn.seeking_venue,
    "seeking_description": artist_btn.seeking_description,
    "image_link":artist_btn.image_link,
    "upcoming_shows": upcoming_shows,
    "past_shows": past_shows,
    "upcoming_shows_count": len(upcoming_shows),
    "past_shows_count": len(past_shows)
  }
  
 # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm(obj=artist)
  # DONE: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist=Artist.query.get_or_404(artist_id)
  form=ArtistForm(obj=artist)
  try:
    artist.name=form.name.data
    artist.city=form.city.data
    artist.state=form.state.data
    artist.phone=form.phone.data
    artist.website_link=form.website_link.data
    artist.facebook_link=form.facebook_link.data
    artist.seeking_venue=form.seeking_venue.data
    artist.seeking_description=form.seeking_description.data
    artist.image_link=form.image_link.data
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully updated!')
  except:
    flash( 'An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()


  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm(obj=venue)

  # DONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm(obj=venue)
  try:
    venue.name= form.name.data # or request.form['name']
    venue.city= form.city.data
    venue.state= form.state.data
    venue.address=form.address.data
    venue.phone= form.phone.data
    venue.genres = form.genres.data
    venue.image_link = form.image_link.data
    venue.facebook_link = form.facebook_link.data
    venue.website_link = form.website_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  except:
    flash( 'An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion
  form=ArtistForm(request.form)
  try:
    new_artist= Artist(
      name= form.name.data,
      city= form.city.data,
      state= form.state.data,
      phone= form.phone.data,
      image_link= form.image_link.data,
      genres= form.genres.data,
      facebook_link= form.facebook_link.data,
      website_link= form.website_link.data,
      seeking_venue= form.seeking_venue.data,
      seeking_description=form.seeking_description.data )
    db.session.add(new_artist)
    db.session.commit()

  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  except:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    print(sys.exc_info())
    db.session.rollback()
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

  # displays list of shows at /shows
  # DONE: replace with real venues data.
  data = []
  shows = Show.query.order_by(Show.start_time.desc()).all()
  for show in shows:
    venue = Venue.query.filter_by(id=show.venue_id).first_or_404()
    artist = Artist.query.filter_by(id=show.artist_id).first_or_404()
    data.extend([{"venue_id": venue.id,"venue_name": venue.name,"artist_id": artist.id,"artist_name": artist.name,
    "artist_image_link": artist.image_link,"start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")  }])

 
  return render_template('pages/shows.html', shows=data)
  

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead
  form = ShowForm(request.form)
  try:

    new_show= Show(artist_id= form.artist_id.data,venue_id= form.venue_id.data,start_time= form.start_time.data)
    db.session.add(new_show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')

  except:

    flash('An error occurred. Show could not be listed.')
    db.session.rollback()

  finally:

    db.session.close()
  # DONE : on unsuccessful db insert, flash an error instead.

    flash('Show was successfully listed!')

  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
