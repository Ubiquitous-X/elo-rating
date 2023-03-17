import os
from flask import Flask
from dotenv import load_dotenv
from models import db

load_dotenv('.env')
SECRET_KEY = os.getenv('SECRET_KEY', 'default')

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['TIMEZONE'] = 'Europe/Stockholm'

db.init_app(app)

with app.app_context():
    db.create_all()

from routes import *

if __name__ == '__main__':
    app.run()