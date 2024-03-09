from app import db 
from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.LargeBinary)
    wins = db.Column(db.Integer)
    losses = db.Column(db.Integer)
    word = db.Column(db.String)
    guesses = relationship("Guesses", uselist=False, back_populates="user")


class Guesses(db.Model, UserMixin):
    __tablename__='guesses'
    user_id = db.Column(db.String, ForeignKey("users.id"), primary_key=True, unique=True)
    guessesInOne = db.Column(db.Integer)
    guessesInTwo = db.Column(db.Integer)
    guessesInThree= db.Column(db.Integer)
    guessesInFour = db.Column(db.Integer)
    guessesInFive = db.Column(db.Integer)
    guessesInSix = db.Column(db.Integer)
    user = relationship("User", back_populates="guesses")