from flask import Blueprint, render_template,request,flash,redirect,url_for
from forms import *
from models import (Venue,db)
import sys
from app import datetime,dateutil


# venues_bp = Blueprint('venue_bp', __name__,template_folder='templates',static_folder='static',static_url_path='assets')
venues_bp = Blueprint('venues_bp', __name__, template_folder='templates',static_folder='static', static_url_path='assets')

#  Venues
#  ----------------------------------------------------------------

@venues_bp.route('/')
def venues():
  # data=[{
  #     "city": "San Francisco",
  #     "state": "CA",
  #     "venues": [{
  #       "id": 1,
  #       "name": "The Musical Hop",
  #       "num_upcoming_shows": 0,
  #     }, {
  #       "id": 3,
  #       "name": "Park Square Live Music & Coffee",
  #       "num_upcoming_shows": 1,
  #     }]
  #   }, {
  #     "city": "New York",
  #     "state": "NY",
  #     "venues": [{
  #       "id": 2,
  #       "name": "The Dueling Pianos Bar",
  #       "num_upcoming_shows": 0,
  #     }]
  #   }]

    data = []
    queried_venues = Venue.query.distinct(Venue.state, Venue.city,).all()
    for queried_venue in queried_venues:
        location = {
            "state": queried_venue.state,
            "city":  queried_venue.city,
        }
        venues = Venue.query.filter_by(state=queried_venue.state,city=queried_venue.city).all()
     
        venue_location = []
        for venue in venues:
            new_venue={}
            new_venue['id'] = venue.id
            new_venue['name']= venue.name
            new_venue['num_upcoming_shows'] = len(venue.shows)
            venue_location.append(new_venue)
        location["venues"] = venue_location
        data.append(location)
    return render_template('pages/venues.html', areas=data);

# @venues.route('/search', methods=['POST'])
# def search_venues():
#   # response={
#   #   "count": 1,
#   #   "data": [{
#   #     "id": 2,
#   #     "name": "The Dueling Pianos Bar",
#   #     "num_upcoming_shows": 0,
#   #   }]
#   # }
  
#   search_term = request.form['search_term']
#   #search venue by name, state or city located
#   search_query = Venue.query.filter(Venue.name.ilike(f'%{search_term}%') | Venue.city.ilike(f'%{search_term}%') | Venue.state.ilike(f'%{search_term}%')) 
#   searched_results = list(search_query)
#   search_term_count = len(searched_results)
#   response={
#       "count":search_term_count,
#       "data":[]
#     }
#   for venue in searched_results:
#       search_result={}
#       search_result["id"] =venue.id
#       search_result["name"] = venue.name
#       search_result["num_upcoming_shows"] =  venue.upcoming_shows_count
#       response["data"].append(search_result)
#   return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@venues_bp.route('/<int:venue_id>')
def show_venue(venue_id):
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  upcoming_shows = []
  past_shows = []
  upcoming_shows_count = 0
  past_shows_count = 0
  present_time =  dateutil.parser.parse(str(datetime.now()))

  for show in venue.shows:
    #finding out if the show is a pasted show or an incoming show
    if dateutil.parser.parse(show.start_time) > present_time:
      upcoming_shows_details={}
      upcoming_shows_details['artist_id'] = show.artist_id
      upcoming_shows_details['artist_name'] = show.artist.name
      upcoming_shows_details['artist_image_link'] = show.artist.image_link
      upcoming_shows_details['start_time'] = show.start_time
      upcoming_shows.append(upcoming_shows_details)
      upcoming_shows_count += 1               
    elif dateutil.parser.parse(show.start_time) < present_time:
      past_shows_details={}
      past_shows_details['artist_id'] = show.artist_id
      past_shows_details['artist_name'] = show.artist.name
      past_shows_details['artist_image_link'] = show.artist.image_link
      past_shows_details['start_time'] = show.start_time
      past_shows.append(past_shows_details)
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

@venues_bp.route('/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@venues_bp.route('/create', methods=['POST'])
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
      seeking_talent = True if request.form.get('seeking_talent') == 'y' else False 
      seeking_description = request.form['seeking_description']


      new_venue = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,facebook_link=facebook_link,website_link=website_link,genres=genres, seeking_talent=seeking_talent,seeking_description=seeking_description)
    
      db.session.add(new_venue)
      db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(error)
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


@venues_bp.route('/<int:venue_id>/delete', methods=['GET'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    venue = Venue.query.get(venue_id)
    try:
      db.session.delete(venue)
      db.session.commit()
      flash(f'Venue was deleted successfully')
    except:
      db.session.rollback()
      flash(f'There was an error while delteing venue')
    finally:
      db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    #return None
    return render_template('pages/home.html')

@venues_bp.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  venue_info=Venue.query.get(venue_id)
  venue={
    "id": venue_info.id,
    "name":venue_info.name,
    "city": venue_info.city,
    "state": venue_info.state,
    "genres": venue_info.genres,
    "phone": venue_info.phone,
    "website_link": venue_info.website_link,
    "facebook_link": venue_info.facebook_link,
    "image_link": venue_info.image_link,
    "seeking_talent":venue_info.seeking_talent,
    "seeking_description": venue_info.seeking_description
  }
  form = VenueForm(obj=venue_info)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@venues_bp.route('/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
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
    #condition for checkbox
    venue.seeking_talent =  True if request.form.get('seeking_talent') == 'y' else False 
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
