# Wordle Project
A basic fullstack web application
------
This is a basic web application that imitates the popular game Wordle. 

# Technologies used:

- Flask <br>
- Python (using pip3 as the package manager) <br>
- SQLAlchemy <br>
- SQLite (engine) <br>
- JavaScript <br>
- HTML<br>
- CSS <br>
- Docker (containerizing project if it isn't already) <br>


# Technology uses:

In this project I used Flask as the web framework, so I could code all of the backend in Python.
I also used the Flask extensions Flask Web Forms (for the signin/signup pages) and Flask-Login to add user functionality. 

For database functionality I chose SQLAlchemy and SQLite because they provide data persistency without actually interacting with 
a database server. Python interacts with the ORM aspect of SQLAlchemy in a way that makes them both easy to work with.

The frontend is mostly raw HTML/CSS with a large part being JavaScript, which dynamically changes elements on the page. 

...in progress

# Resources used in project

> "valid-wordle-words.txt" 

Used to check the guesses to determine if the word is a valid 5 letter word.
Source: https://www.kaggle.com/datasets/bcruise/wordle-valid-words?resource=download


> "valid_solutions.cvs" 

This is a list of common 5 letter words that are chosen as 
possible words that the user must guess.
Source: https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93



