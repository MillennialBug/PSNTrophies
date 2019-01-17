from flask import Flask
from sys import platform
from flask_sqlalchemy import SQLAlchemy
from auth import engine_address_trophies

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = engine_address_trophies
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

class trophies(db.Model):
    __tablename__ = 'trophies'
    Number        = db.Column('Number', db.Integer)
    Game          = db.Column('Game',   db.Unicode, primary_key=True)
    Name          = db.Column('Name',   db.Unicode, primary_key=True)
    Text          = db.Column('Text',   db.Unicode)
    Date          = db.Column('Date',   db.Unicode)
    Time          = db.Column('Time',   db.Unicode)
    Rank          = db.Column('Rank',   db.Unicode)
    TrophyImage   = db.Column('TrophyImage',  db.Unicode)
    GameImage     = db.Column('GameImage',    db.Unicode)

