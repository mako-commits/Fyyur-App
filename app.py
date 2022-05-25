#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
from unittest import result
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from sqlalchemy import ForeignKey
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app,db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(500))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(500))   
    seeking_talent = db.Column(db.Boolean(),default=False)
    seeking_description = db.Column(db.String(500))
    upcoming_shows_count = db.Column(db.Integer, default=0)
    past_shows_count = db.Column(db.Integer, default=0)
    shows= db.relationship('Show', backref='venue', lazy=True ,cascade='save-update, merge, delete')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    upcoming_shows_count = db.Column(db.Integer, default=0)
    past_shows_count = db.Column(db.Integer, default=0)
    shows= db.relationship('Show', backref='artist', lazy=True, cascade='save-update, merge, delete')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key= True)
  artist_id = db.Column(db.Integer, ForeignKey(Artist.id),nullable=False)
  venue_id =  db.Column(db.Integer, ForeignKey(Venue.id),nullable=False)
  start_time = db.Column(db.String, nullable=True)
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
  ####NOTE-REWRITE
    data = []
    queried_venues = Venue.query.distinct(Venue.state, Venue.city,).all()
    for queried_venue in queried_venues:
        location = {
            "state": queried_venue.state,
            "city":  queried_venue.city,
        }
        venues = Venue.query.filter_by(state=queried_venue.state,city=queried_venue.city).all()

       
        new_venue_location = []
        for venue in venues:
            new_venue={}
            new_venue['id'] = venue.id
            new_venue['name']= venue.name
            new_venue['num_upcoming_shows'] = len(venue.shows)
            new_venue_location.append(new_venue)
        location["venues"] = new_venue_location
        data.append(location)
    return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  results = list(Venue.query.filter(Venue.name.ilike("%" + request.form['search_term'] + "%")))
  response={
      "count":len(results),
      "data":[]
    }
  for venue in results:
      response["data"].append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": venue.upcoming_shows_count
      })
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  past_shows = []
  past_shows_count = 0
  upcoming_shows = []
  upcoming_shows_count = 0
  present_time =  dateutil.parser.parse(str(datetime.now()))

  for show in venue.shows:
    if dateutil.parser.parse(show.start_time) > present_time:
      upcoming_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": show.artist.name,
                    "artist_image_link": show.artist.image_link,
                    "start_time": show.start_time
                })
      upcoming_shows_count += 1               
    elif dateutil.parser.parse(show.start_time) < present_time:
                past_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": show.artist.name,
                    "artist_image_link": show.artist.image_link,
                    "start_time": show.start_time
                })
                past_shows_count += 1

  data={
    "id": venue.id,
    "name": venue.name,
    "genres":venue.genres.split(','),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows_count": past_shows_count,
    "upcoming_shows_count": upcoming_shows_count,
    "upcoming_shows": upcoming_shows,
     "past_shows": past_shows
   
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
  # TODO: modify data to be the data object returned from db insertion
    error = False
    try:
      name = request.form['name']
      city = request.form['city']
      state = request.form['state']
      address = request.form['address']
      phone = request.form['phone']
      image_link = request.form['image_link']
      facebook_link = request.form['facebook_link']
      website_link = request.form['website_link']
      genres =','.join(request.form.getlist('genres')) 
      seeking_talent = True if request.form['seeking_talent'] == 'y' else False
      seeking_description = request.form['seeking_description']


      new_venue = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,facebook_link=facebook_link,website_link=website_link,genres=genres, seeking_talent=seeking_talent, seeking_description=seeking_description)
    
      db.session.add(new_venue)
      db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
        if error:
            # TODO: on unsuccessful db insert, flash an error instead. 
            flash('An error occured. Venue ' + request.form['name'] + ' Could not be listed!')
        else:   
            # on successful db insert, flash success 
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')


@app.route('/venues/delete/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    # venue = Venue.query.get(venue_id)
    # db.session.delete(venue)
    # db.session.commit()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    return None
    # return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data= []
  data = Artist.query.distinct(Artist.name).all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  results = list(Artist.query.filter(Artist.name.ilike("%" + request.form['search_term'] + "%")))
  response={
      "count":len(results),
      "data":[]
    }
  for artist in results:
      response["data"].append({
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": artist.upcoming_shows_count
      })
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.get(artist_id)
  past_shows = []
  past_shows_count = 0
  upcoming_shows = []
  upcoming_shows_count = 0
  present_time =  dateutil.parser.parse(str(datetime.now()))

  for show in artist.shows:
    if  dateutil.parser.parse(show.start_time) > present_time:
      upcoming_shows.append({
         "artist_id": show.artist_id,
          "artist_name": show.artist.name,
          "artist_image_link": show.artist.image_link,
          "start_time": show.start_time
      })
      upcoming_shows_count += 1
    elif dateutil.parser.parse(show.start_time) < present_time:    
                past_shows.append({
                    "artist_id": show.artist_id,
                    "artist_name": show.artist.name,
                    "artist_image_link": show.artist.image_link,
                    "start_time": show.start_time
                })
                past_shows_count += 1

  artist_data={
    'id': artist.id,
    "name": artist.name,
    "genres":artist.genres.split(','),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows":past_shows,
    "past_shows_count":past_shows_count,
    "upcoming_shows":upcoming_shows,
    "upcoming_shows_count":upcoming_shows_count  
  }
  return render_template('pages/show_artist.html', artist=artist_data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):  
  artist_info=Artist.query.get(artist_id)  
  artist={
    "id": artist_info.id,
    "name": artist_info.name,
    "genres": artist_info.genres,
    "city": artist_info.city,
    "state": artist_info.state,
    "phone": artist_info.phone,
    "website_link": artist_info.website_link,
    "facebook_link": artist_info.facebook_link,
    "image_link": artist_info.image_link,
    "seeking_venue": artist_info.seeking_venue,
    "seeking_description": artist_info.seeking_description
  }
  form = ArtistForm(obj=artist_info)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
 artist = Artist.query.get(artist_id)
 error = False
 try: 
    artist.name = request.form['name']
    artist.genres = request.form['genres']
    artist.state = request.form['state']
    artist.city = request.form['city']
    artist.phone = request.form['phone']
    artist.website_link = request.form['website_link']
    artist.facebook_link = request.form['facebook_link']
    artist.seeking_venue = bool(request.form['seeking_venue'])
    artist.seeking_description = request.form['seeking_description']
    artist.image_link= request.form['image_link']
    db.session.commit()
 except:
   error = True
   db.session.rollback()
 finally:
  db.session.close()
  if error:
     flash("Oops....Something isn't right")
  else:
    flash("Artist " + request.form['name'] + " was edited succesfully")
 return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue_info=Venue.query.get(venue_id)
  venue={
    "id": venue_info.id,
    "name":venue_info.name,
    "city": venue_info.city,
    "state": venue_info.state,
    "phone": venue_info.phone,
    "website_link": venue_info.website_link,
    "facebook_link": venue_info.facebook_link,
    "image_link": venue_info.image_link,
    "seeking_talent":venue_info.seeking_talent,
    "seeking_description": venue_info.seeking_description
  }
  form = VenueForm(obj=venue_info)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venue = Venue.query.get(venue_id)
  error = False
  try:  
    venue.name = request.form['name']
    venue.genres = request.form['genres']
    venue.state = request.form['state']
    venue.city = request.form['city']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.website_link = request.form['website_link']
    venue.facebook_link = request.form['facebook_link']
    venue.seeking_venue = bool(request.form['seeking_venue'])
    venue.seeking_description = request.form['seeking_description']
    venue.image_link= request.form['image_link']
    db.session.commit()
  except:
   error = True
   db.session.rollback()
  finally:
   db.session.close()
  if error:
     flash("Oops....Something isn't right")
  else:
    flash("Venue " + request.form['name'] + " was edited succesfully")
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
    error = False
    try: 
      name = request.form['name']
      city = request.form['city']
      state = request.form['state']
      phone = request.form['phone']
      image_link = request.form['image_link']
      facebook_link = request.form['facebook_link']
      website = request.form['website_link']
      genres =','.join(request.form.getlist('genres')) 
      seeking_venue = bool(request.form['seeking_venue'])
      seeking_description = request.form['seeking_description']
    
      new_artist = Artist(name=name,city=city,state=state,phone=phone,image_link=image_link,facebook_link=facebook_link,website_link=website,genres=genres, seeking_venue=seeking_venue, seeking_description=seeking_description)
    
      db.session.add(new_artist)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()
      if error:
           # TODO: on unsuccessful db insert, flash an error instead.
          flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
      else:    
           # on successful db insert, flash success
          flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
  

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data= []
  shows = Show.query.all()
  for show in shows:
    data.append({
      "venue_id": show.venue.id,
      "venue_name": show.venue.name,
      "artist_id": show.artist.id,
      "artist_name":show.artist.name,
     "artist_image_link": show.artist.image_link,
     "start_time": show.start_time
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
    error = False
    try:
      artist_id= request.form['artist_id']
      venue_id= request.form['venue_id']
      start_time = request.form['start_time']
      show = Show(artist_id=artist_id,venue_id=venue_id,start_time=start_time)
      db.session.add(show)
      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()
      if error:
        flash('An error occurred. Show could not be listed.')
      else:
        # on successful db insert, flash success
        flash('Show was successfully listed!')
        # TODO: on unsuccessful db insert, flash an error instead.
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
