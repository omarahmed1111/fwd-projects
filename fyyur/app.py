#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sys
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import Artist, Venue, Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
db.init_app(app)

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

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
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  indexes = {}
  venues = Venue.query.all()
  ind = 0
  dateTimeObj = datetime.now()
  timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")
  for venue in venues:
    if venue.city in indexes:
      cur_ind = indexes[venue.city]
      data[cur_ind]['venues'].append({
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows': Show.query.filter(venue.id==Show.venue_id, Show.start_time > timestampStr).count()
      })
    else:
      indexes[venue.city] = ind
      data.append({
        'city': venue.city,
        'state': venue.state,
        'venues': [{
          'id': venue.id,
          'name': venue.name,
          'num_upcoming_shows': Show.query.filter(venue.id==Show.venue_id, Show.start_time > timestampStr).count()
        }] 
      })
      ind = ind + 1

      
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike("%"+search_term+"%")).all()
  response = {
    'count': 0,
    'data': []
  }
  dateTimeObj = datetime.now()
  timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")
  for venue in venues:
    response['count'] = response['count'] + 1
    response['data'].append({
      'id': venue.id,
      'name': venue.name,
      'num_upcoming_shows': Show.query.filter(venue.id==Show.venue_id, Show.start_time > timestampStr).count()
    })
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  dateTimeObj = datetime.now()
  timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")
  venue = Venue.query.get(venue_id)
  data = {
    'id': venue.id,
    'name': venue.name,
    'genres': venue.genres,
    'address': venue.address,
    'city': venue.city,
    'state': venue.state,
    'phone': venue.phone,
    'website': venue.website,
    'facebook_link': venue.facebook_link,
    'seeking_talent': venue.seeking_talent,
    'seeking_description': venue.seeking_description,
    'image_link': venue.image_link,
    'past_shows': [],
    'upcoming_shows': [],
    'past_shows_count': Show.query.filter(venue.id==Show.venue_id, Show.start_time < timestampStr).count(),
    'upcoming_shows_count': Show.query.filter(venue.id==Show.venue_id, Show.start_time > timestampStr).count()
  }
  
  pshows = db.session.query(Artist, Show).join(Artist).filter(Show.start_time < timestampStr, venue.id == Show.venue_id).all()
  for show in pshows:
    data['past_shows'].append({
      'artist_id': show[1].artist_id,
      'artist_name': show[0].name,
      'artist_image_link': show[0].image_link,
      'start_time': show[1].start_time
    })
  fshows = db.session.query(Artist, Show).join(Artist).filter(Show.start_time > timestampStr, venue.id == Show.venue_id).all()
  for show in fshows:
    data['upcoming_shows'].append({
      'artist_id': show[1].artist_id,
      'artist_name': show[0].name,
      'artist_image_link': show[0].image_link,
      'start_time': show[1].start_time
    })  
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
  # TODO: modify data to be the data object returned from db insertion
  venue = {}
  venue['name'] = request.form.get('name', '')
  venue['city'] = request.form.get('city', '')
  venue['state'] = request.form.get('state', '')
  venue['address'] = request.form.get('address', '')
  venue['phone'] = request.form.get('phone', '')
  venue['genres'] = ','.join(request.form.getlist('genres'))
  venue['facebook_link'] = request.form.get('facebook_link', '')
  
  error = False
  try:
    venue = Venue(**venue)
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  if(not error):  
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:  
  # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    Venue.query.filter_by(id = venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()    
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return 'Deleted'

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = []
  artists = Artist.query.all()
  for artist in artists:
    data.append({
      'id': artist.id,
      'name': artist.name
    })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike("%"+search_term+"%")).all()
  response = {
    'count': 0,
    'data': []
  }
  dateTimeObj = datetime.now()
  timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")
  for artist in artists:
    response['count'] = response['count'] + 1
    response['data'].append({
      'id': artist.id,
      'name': artist.name,
      'num_upcoming_shows': Show.query.filter(artist.id==Show.artist_id, Show.start_time > timestampStr).count()
    })
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  dateTimeObj = datetime.now()
  timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S")
  artist = Artist.query.get(artist_id)
  data = {
    'id': artist.id,
    'name': artist.name,
    'genres': artist.genres,
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'website': artist.website,
    'facebook_link': artist.facebook_link,
    'seeking_venue': artist.seeking_venue,
    'seeking_description': artist.seeking_description,
    'image_link': artist.image_link,
    'past_shows': [],
    'upcoming_shows': [],
    'past_shows_count': Show.query.filter(artist.id==Show.artist_id, Show.start_time < timestampStr).count(),
    'upcoming_shows_count': Show.query.filter(artist.id==Show.artist_id, Show.start_time > timestampStr).count()
  }
  
  pshows = db.session.query(Venue, Show).join(Venue).filter(Show.start_time < timestampStr, artist.id == Show.artist_id).all()
  
  for show in pshows:
    data['past_shows'].append({
      'venue_id': show[1].venue_id,
      'venue_name': show[0].name,
      'venue_image_link': show[0].image_link,
      'start_time': show[1].start_time
    })
  fshows = db.session.query(Venue, Show).join(Venue).filter(Show.start_time > timestampStr, artist.id == Show.artist_id).all()
  for show in fshows:
    data['upcoming_shows'].append({
      'venue_id': show[1].venue_id,
      'venue_name': show[0].name,
      'venue_image_link': show[0].image_link,
      'start_time': show[1].start_time
    })
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  
  # TODO: populate form with fields from artist with ID <artist_id>
  data = {
    'id': artist.id,
    'name': artist.name,
    'genres': artist.genes,
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'website': artist.website,
    'facebook_link': artist.facebook_link,
    'seeking_venue': artist.seeking_venue,
    'seeking_description': artist.seeking_description,
    'image_link': artist.image_link
  }

  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist = Artist.query.get(artist_id)
  artist.name = request.form.get('name', '')
  artist.genres = ','.join(request.form.getlist('genres'))
  artist.city = request.form.get('city', '')
  artist.state = request.form.get('state', '')
  artist.phone = request.form.get('phone', '')
  artist.website = request.form.get('website', '')
  artist.facebook_link = request.form.get('facebook_link', '')
  artist.seeking_venue = request.form.get('seeking_venue', '')
  artist.seeking_description = request.form.get('seeking_description', '')
  artist.image_link = request.form.get('image_link', '')
  db.session.commit()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  
  # TODO: populate form with values from venue with ID <venue_id>
  data = {
    'id': venue.id,
    'name': venue.name,
    'genres': venue.genes,
    'address': venue.address,
    'city': venue.city,
    'state': venue.state,
    'phone': venue.phone,
    'website': venue.website,
    'facebook_link': venue.facebook_link,
    'seeking_venue': venue.seeking_venue,
    'seeking_description': venue.seeking_description,
    'image_link': venue.image_link
  }
  
  return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  venue.name = request.form.get('name', '')
  venue.genres = ','.join(request.form.getlist('genres'))
  venue.address = request.form.get('address', '')
  venue.city = request.form.get('city', '')
  venue.state = request.form.get('state', '')
  venue.phone = request.form.get('phone', '')
  venue.website = request.form.get('website', '')
  venue.facebook_link = request.form.get('facebook_link', '')
  venue.seeking_venue = request.form.get('seeking_venue', '')
  venue.seeking_description = request.form.get('seeking_description', '')
  venue.image_link = request.form.get('image_link', '')
  db.session.commit()
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
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  artist = {}
  artist['name'] = request.form.get('name', '')
  artist['city'] = request.form.get('city', '')
  artist['state'] = request.form.get('state', '')
  artist['phone'] = request.form.get('phone', '')
  artist['genres'] = ','.join(request.form.getlist('genres'))
  artist['facebook_link'] = request.form.get('facebook_link', '')
  error = False
  try:
    artist = Artist(**artist)
    db.session.add(artist)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  if(not error):  
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:  
  # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  data = []
  shows = Show.query.all()
  for show in shows:
    artist = Artist.query.get(show.artist_id)
    venue = Venue.query.get(show.venue_id)
    data.append({
      'venue_id': venue.id,
      'venue_name': venue.name,
      'artist_id': artist.id,
      'artist_name': artist.name,
      'artist_image_link': artist.image_link,
      'start_time': show.start_time
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  show = {}
  show['artist_id'] = request.form.get('artist_id', '')
  show['venue_id'] = request.form.get('venue_id', '')
  show['start_time'] = request.form.get('start_time', '')
  error = False
  try:
    data = Show(**show)
    db.session.add(data)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  if(not error):  
    # on successful db insert, flash success
    flash('Show ' + ' was successfully listed!')
  else:  
  # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show ' + ' could not be listed.')
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
