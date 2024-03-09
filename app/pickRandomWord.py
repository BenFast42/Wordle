from random import randint
from app.generateDictionaries import solutionsDict

def pickRandomWord():
    randomKey = randint(1, len(solutionsDict))
    randomWord = solutionsDict[randomKey]
    return randomWord

