import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///fyyurapp.db'
# SQLALCHEMY_DATABASE_URI = 'postgresql://<username>:<Password>@localhost:5432/<DB_Name>'
