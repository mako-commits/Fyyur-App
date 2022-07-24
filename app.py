#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import sys
from unittest import result
import dateutil.parser
import babel
from flask import (Flask, render_template, request, Response, flash,
                   redirect, url_for)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from markupsafe import Markup
from requests import session
from sqlalchemy import desc
from forms import *
from flask_migrate import Migrate
from models import (Venue, Artist, Show, db)
from flask_wtf.csrf import CSRFProtect
from jinja2.utils import markupsafe 
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
db.app = app
csrf = CSRFProtect(app)

markupsafe.Markup()
Markup('')
# ! drops the database tables and starts fresh can be used to initialize a clean database
# db.drop_all()
# db.create_all()
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    new_venues = Venue.query.order_by(desc(Venue.created_at)).limit(10).all()
    new_artists = Artist.query.order_by(
        desc(Artist.created_at)).limit(10).all()
    return render_template(
        'pages/home.html',
        venues=new_venues,
        artists=new_artists)


# #  Venues
# #  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    data = []
    queried_venues = Venue.query.distinct(Venue.state, Venue.city,).all()
    for queried_venue in queried_venues:
        location = {
            "state": queried_venue.state,
            "city": queried_venue.city,
        }
        venues = Venue.query.filter_by(
            state=queried_venue.state,
            city=queried_venue.city).all()

        venue_location = []
        for venue in venues:
            new_venue = {}
            new_venue['id'] = venue.id
            new_venue['name'] = venue.name
            new_venue['num_upcoming_shows'] = len(venue.shows)
            venue_location.append(new_venue)
        location["venues"] = venue_location
        data.append(location)
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form['search_term']
    # search venue by name, state or city located
    search_query = Venue.query.filter(Venue.name.ilike(f'%{search_term}%') | Venue.city.ilike(
        f'%{search_term}%') | Venue.state.ilike(f'%{search_term}%'))
    searched_results = list(search_query)
    search_term_count = len(searched_results)
    response = {
        "count": search_term_count,
        "data": []
    }
    for venue in searched_results:
        search_result = {}
        search_result["id"] = venue.id
        search_result["name"] = venue.name
        search_result["num_upcoming_shows"] = venue.upcoming_shows_count
        response["data"].append(search_result)
    return render_template(
        'pages/search_venues.html',
        results=response,
        search_term=request.form.get(
            'search_term',
            ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get(venue_id)
    present_time = str(datetime.now())

    past_shows_query = db.session.query(Show).join(Artist).filter(
        Show.venue_id == venue_id).filter(
        Show.start_time < present_time).all()
    past_shows = []

    for show in past_shows_query:
        past_shows.append({
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time
        })
    past_shows_count = len(past_shows)

    upcoming_shows_query = db.session.query(Show).join(Artist).filter(
        Show.venue_id == venue_id).filter(
        Show.start_time > present_time).all()
    upcoming_shows = []

    for show in upcoming_shows_query:
        upcoming_shows.append({
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": show.start_time
        })
    upcoming_shows_count = len(upcoming_shows)

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres.split(','),
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website_link,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "past_shows_count": past_shows_count,
        "upcoming_shows": upcoming_shows,
        "upcoming_shows_count": upcoming_shows_count,
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
    form = VenueForm(request.form)
    if form.validate_on_submit():
        try:
            venue = Venue(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                address=form.address.data,
                phone=form.phone.data,
                genres=",".join(form.genres.data),
                facebook_link=form.facebook_link.data,
                image_link=form.image_link.data,
                seeking_talent=form.seeking_talent.data,
                seeking_description=form.seeking_description.data,
                website_link=form.website_link.data
            )
            db.session.add(venue)
            db.session.commit()
            flash(
                'Venue ' +
                request.form['name'] +
                ' was successfully listed!')
        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
            flash(
                'An error occurred. Venue' +
                request.form['name'] +
                ' could not be listed.')
        finally:
            db.session.close()
    else:
        print("\n\n", form.errors)
        flash(
            'An error occurred. Venue' +
            request.form['name'] +
            ' could not be listed.')
        flash(form.errors)
    return render_template('pages/home.html', form=form)


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get(venue_id)
    form = VenueForm(obj=venue)
    form.genres.data = venue.genres.split(",")
    venue = {
        "id": venue_id,
        "name": venue.name,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website_link": venue.website_link,
        "facebook_link": venue.facebook_link,
        "image_link": venue.image_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description
    }
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    error = False

    form = VenueForm(request.form)
    if form.validate_on_submit():
        try:
            venue = Venue.query.get(venue_id)
            venue.name = form.name.data
            venue.genres = ",".join(form.genres.data)
            venue.state = form.state.data
            venue.city = form.city.data
            venue.address = form.address.data
            venue.phone = form.phone.data
            venue.website_link = form.website_link.data
            venue.facebook_link = form.facebook_link.data
            venue.seeking_talent = form.seeking_talent.data
            venue.seeking_description = form.seeking_description.data
            venue.image_link = form.image_link.data
            db.session.commit()
        except BaseException:
            error = True
            print(sys.exc_info())
            db.session.rollback()
        finally:
            db.session.close()
    if error:
        flash("Error....Something isn't right")
    else:
        flash("Venue " + request.form['name'] + " was edited succesfully")
    return redirect(url_for('show_venue', venue_id=venue_id))


@app.route('/venues/<int:venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
    venue = Venue.query.get(venue_id)
    try:
        db.session.delete(venue)
        db.session.commit()
        flash(f'Venue was deleted successfully')
    except BaseException:
        db.session.rollback()
        flash(f'There was an error while delteing venue')
    finally:
        db.session.close()
    return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------


@app.route('/artists')
def artists():
    data = Artist.query.distinct(Artist.name).all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form['search_term']
    # search artist by name or city
    search_query = Artist.query.filter(Artist.name.ilike(f'%{search_term}%') | Artist.city.ilike(
        f'%{search_term}%') | Artist.state.ilike(f'%{search_term}%'))
    searched_results = list(search_query)
    search_term_count = len(searched_results)
    response = {
        "count": search_term_count,
        "data": []
    }
    for artist in searched_results:
        search_result = {}
        search_result["id"] = artist.id
        search_result["name"] = artist.name
        search_result["num_upcoming_shows"] = artist.upcoming_shows_count
        response["data"].append(search_result)
    return render_template(
        'pages/search_artists.html',
        results=response,
        search_term=request.form.get(
            'search_term',
            ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    present_time = str(datetime.now())

    past_shows_query = db.session.query(Show).join(Venue).filter(
        Show.artist_id == artist_id).filter(
        Show.start_time < present_time).all()
    past_shows = []

    for show in past_shows_query:
        past_shows.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time
        })
    past_shows_count = len(past_shows)

    upcoming_shows_query = db.session.query(Show).join(Venue).filter(
        Show.artist_id == artist_id).filter(
        Show.start_time > present_time).all()
    upcoming_shows = []

    for show in upcoming_shows_query:
        upcoming_shows.append({
            "venue_id": show.venue_id,
            "venue_name": show.venue.name,
            "venue_image_link": show.venue.image_link,
            "start_time": show.start_time
        })
    upcoming_shows_count = len(upcoming_shows)

    data = {
        'id': artist.id,
        "name": artist.name,
        "genres": artist.genres.split(','),
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "past_shows_count": past_shows_count,
        "upcoming_shows": upcoming_shows,
        "upcoming_shows_count": upcoming_shows_count
    }
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(obj=artist)
    form.genres.data = artist.genres.split(",")
    artist = {
        "id": artist_id,
        "name": artist.name,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website_link": artist.website_link,
        "facebook_link": artist.facebook_link,
        "image_link": artist.image_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description
    }
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    error = False
    artist = Artist.query.get(artist_id)
    form = ArtistForm(request.form)

    if form.validate_on_submit():
        try:
            artist.name = form.name.data
            artist.city = form.city.data
            artist.state = form.state.data
            artist.phone = form.phone.data
            artist.genres = ",".join(form.genres.data)
            artist.facebook_link = form.facebook_link.data
            artist.image_link = form.image_link.data
            artist.website_link = form.website_link.data
            artist.seeking_venue = form.seeking_venue.data
            artist.seeking_description = form.seeking_description.data
            db.session.commit()
        except BaseException:
            error = True
            print(sys.exc_info())
            db.session.rollback()
        finally:
            db.session.close()
    if error:
        flash("Oops....Something isn't right")
    else:
        flash("Venue " + request.form['name'] + " was edited succesfully")
    return redirect(url_for('show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)
    if form.validate_on_submit():
        try:
            artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                genres=",".join(form.genres.data),
                facebook_link=form.facebook_link.data,
                image_link=form.image_link.data,
                seeking_venue=form.seeking_venue.data,
                seeking_description=form.seeking_description.data,
                website_link=form.website_link.data
            )
            db.session.add(artist)
            db.session.commit()
            flash(
                'Artist ' +
                request.form['name'] +
                ' was successfully listed!')
        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
            flash(
                'An error occurred. Artist ' +
                request.form['name'] +
                ' could not be listed.')
        finally:
            db.session.close()
    else:
        print("\n\n", form.errors)
        flash(
            'An error occurred. Artist ' +
            request.form['name'] +
            ' could not be listed.')
        flash(form.errors)
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    data = []
    shows = Show.query.all()
    for show in shows:
        data.append({
            "venue_id": show.venue.id,
            "venue_name": show.venue.name,
            "artist_id": show.artist.id,
            "artist_name": show.artist.name,
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
    form = ShowForm(request.form)
    if form.validate_on_submit():
        try:
            show = Show(
                artist_id=form.artist_id.data,
                venue_id=form.venue_id.data,
                start_time=form.start_time.data
            )
            db.session.add(show)
            db.session.commit()
            flash('Show was successfully listed!')
        except BaseException:
            db.session.rollback()
            print(sys.exc_info())
            flash('An error occurred. Show could not be listed.')
        finally:
            db.session.close()
    else:
        print("\n\n", form.errors)
        flash('An error occurred. Show could not be listed.')
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(400)
def server_error(error):
    return render_template('errors/400.html'), 400


@app.errorhandler(409)
def server_error(error):
    return render_template('errors/409.html'), 409


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
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

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)

