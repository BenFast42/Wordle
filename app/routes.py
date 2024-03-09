from app import app, db, load_user
from app.models import User, Guesses
from app.forms import SignUpForm, SignInForm
from flask import render_template, redirect, url_for, request, flash, session, jsonify, make_response
from flask_login import login_required, login_user, logout_user, current_user
import bcrypt
from app.generateDictionaries import generateGuessDict, generateSolutionDict, guessDict, solutionsDict
from app.pickRandomWord import pickRandomWord
from app.compareWords import compareWords
from app.dataBaseSetup import InitializeGuesses


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index(): 

    session['wordset'] = False
    #if dictionaries are empty, generate them
    if not guessDict and not solutionsDict:
        generateGuessDict()
        generateSolutionDict()

    return render_template('index.html')

@app.route('/users/signin', methods=['GET', 'POST'])
def users_signin():
    signin = SignInForm()
    if signin.validate_on_submit():
        user = load_user(signin.id.data)
        if user:
            # Check if the provided password matches the hashed password in the database
            password = signin.password.data.encode('UTF-8')
            if bcrypt.checkpw(password, user.password):
                
                login_user(user)
                #Initalize Wins/losses as zero in database

                if not user.wins:
                    user.wins = 0
                    db.session.commit()
                if not user.losses:
                    user.losses = 0
                    db.session.commit()
                
                #Initalize guesses table in database to be zero
                guesses = Guesses.query.filter_by(user_id=user.id).first()
                if guesses is None: 
                    InitializeGuesses(user.id)

                return redirect('/wordle') 
            else:
                flash("Error: Password is incorrect", 'error')
                return redirect(url_for('users_signin'))
        else:
            flash("Error: User not found", 'error')
            return redirect(url_for('users_signin'))
        
         
    return render_template('users_signin.html', form=signin)


# sign-up functionality
@app.route('/users/signup', methods=['GET', 'POST'])
def users_signup():
    signup = SignUpForm()
    if signup.validate_on_submit():
        #if passwords match
        password = signup.password.data 
        if signup.password.data == signup.password_confirm.data:
            hashedpwd = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()) #salt and hash password here
        else:
            flash('Error: Passwords do not match', 'error')
            return redirect(url_for('users_signup'))
        
        #pass user into User class
        userinfo = User(id=signup.id.data, name=signup.name.data, password=hashedpwd)

        #pass user info into the database, if already there alert user
        try:
            db.session.add(userinfo)
            db.session.commit()
            return redirect('/index')
        except: 
            flash('Error: User already exists', 'error')
            return redirect(url_for('users_signup'))
        
    return render_template('users_signup.html', form=signup)
    

# sign-out functionality 
@app.route('/users/signout', methods=['GET', 'POST'])
def users_signout():
    if users_signout:
        logout_user()
    return redirect('/index')


@login_required
@app.route('/wordle', methods=['GET', 'POST'])
def wordle():
    user = current_user

    # Sent from wordle.html to indicate a game has concluded and to clear the answer and "colors" list
    if request.method == 'POST':
        #Reponse in expected form: {'gameEnd': True, 'win': True, 'loss': False} Example of a successful guess
        data = request.json
        status = data['gameEnd']
        if status == True:
            if user.word:
                session['wordset'] = False
                user.word = None
                db.session.commit()

            if 'colors' in session:
                session.pop('colors')
            
        if data['win'] == True:
            user.wins += 1
        elif data['loss'] == True:
            user.losses += 1
        db.session.commit()
    
    if session['wordset'] == False:
        user.word = pickRandomWord()
        print(f'New word {user.word}')#Test print statement
        session['wordset'] = True
        db.session.commit()

    guess_dict_json = jsonify(guessDict).get_data(as_text=True)

    if session.get('colors'): 
        return render_template('wordle.html', colors=session['colors'], guess_dict_json=guess_dict_json, userName=user.name)
    
    return render_template('wordle.html', guess_dict_json=guess_dict_json, userName=user.name)


@login_required
@app.route('/processGuess', methods=['GET', 'POST'])
def processGuess():
    user = current_user
    if request.method == "POST":
        data = request.json
        word = data[0]
        guess = word
        answer = user.word 
        print(answer)
        session['colors'] = compareWords(guess, answer)
        return jsonify([session['colors'], answer])


@login_required  
@app.route('/processStats', methods=['POST', 'GET'])
def processStats():
    user = current_user
    if request.method == "POST":
        data = request.json
        guessNumber = data["guessNumber"]

        if guessNumber == 1:
            user.guesses.guessesInOne += 1
    
        elif  guessNumber == 2:
            user.guesses.guessesInTwo += 1

        elif  guessNumber == 3:
           user.guesses.guessesInThree += 1

        elif  guessNumber == 4:
           user.guesses.guessesInFour += 1

        elif  guessNumber == 5:
           user.guesses.guessesInFive += 1

        else:
            user.guesses.guessesInSix += 1

        db.session.commit()
        return "Success", 200


@login_required 
@app.route('/users/stats', methods=['GET', 'POST'])
def stats():
    user = current_user
    guessesDict = {
        "one" : user.guesses.guessesInOne,
        "two" : user.guesses.guessesInTwo,
        "three" : user.guesses.guessesInThree,
        "four" : user.guesses.guessesInFour,
        "five" : user.guesses.guessesInFive,
        "six" : user.guesses.guessesInSix
    }
    total = user.wins+user.losses
    winrate = {
        'wins': user.wins, 
        'losses': user.losses, 
        'total': total
    }

    return render_template("stats.html", guessesDict=guessesDict, winrate=winrate)
    