import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
# class Database_URI:
#     database_name = 'fyyurapp'
#     username = 'postgres'
#     password = 'Pass123$'
#     url = 'localhost:5432'
#     SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(username,password,url,database_name)

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Pass123$@localhost:5432/fyyurapp'
