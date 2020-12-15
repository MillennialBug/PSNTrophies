from flask import Flask
from sys import platform
from flask_sqlalchemy import SQLAlchemy
from auth import database_addr

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_addr
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
    GameHex       = db.Column('GameHex', db.Unicode, primary_key=True)
    TrophyImage   = db.Column('TrophyImage',  db.Unicode)
    GameImage     = db.Column('GameImage',    db.Unicode)
    User          = db.Column('User', db.Unicode)

