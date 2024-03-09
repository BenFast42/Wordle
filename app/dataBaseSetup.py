from app.models import Guesses
from app import db

def InitializeGuesses(userid):
    InitialGuesses = Guesses(
        user_id = userid,
        guessesInOne = 0,
        guessesInTwo = 0,
        guessesInThree = 0,
        guessesInFour = 0,
        guessesInFive= 0,
        guessesInSix = 0
    )
    db.session.add(InitialGuesses)
    db.session.commit()