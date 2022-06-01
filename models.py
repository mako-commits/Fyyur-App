from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import ForeignKey
from datetime import datetime

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(500), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    website_link = db.Column(db.String(500), nullable=False)   
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(500), nullable=False)
    upcoming_shows_count = db.Column(db.Integer, default=0, nullable=False)
    past_shows_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    shows= db.relationship('Show', backref='venue', lazy=True ,
    cascade="all,delete,delete-orphan")

    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.city} {self.address} {self.phone} {self.genres} {self.facebook_link} {self.image_link} {self.website_link} {self.seeking_description} {self.seeking_talent} {self.past_shows_count} {self.past_shows_count}>'
    

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120), nullable=False)
    facebook_link = db.Column(db.String(120), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    website_link = db.Column(db.String(120), nullable=False)
    seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
    seeking_description = db.Column(db.String(500), nullable=False)
    upcoming_shows_count = db.Column(db.Integer, default=0, nullable=False)
    past_shows_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    shows= db.relationship('Show', backref='artist', lazy=True, cascade="all,delete,delete-orphan")


    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.city}  {self.phone} {self.genres} {self.facebook_link} {self.image_link} {self.website_link} {self.seeking_description} {self.seeking_venue} {self.past_shows_count} {self.past_shows_count}>'
    

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key= True)
  artist_id = db.Column(db.Integer, ForeignKey(Artist.id),nullable=False)
  venue_id =  db.Column(db.Integer, ForeignKey(Venue.id),nullable=False)
  start_time = db.Column(db.String, nullable=True)
 
  def __repr__(self):
        return f'<Show {self.id} {self.artist_id} {self.venue_id} {self.start_time}>'

