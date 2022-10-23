"""Server for movie ratings app."""

from crypt import methods
from flask import (Flask, render_template, request, flash, session, redirect)
from model import connect_to_db, db, Rating
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def show_homepage():
    """Goes to homepage"""

    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    """Show all movies"""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def show_movie_information(movie_id):
    """Shows details for individual movie"""

    movie = crud.get_movies_by_id(movie_id)
    
    return render_template('movie_details.html', movie=movie)

@app.route('/users')
def show_user_information():
    """Show details for user information"""

    users = crud.get_users()

    return render_template('all_users.html', users=users)

@app.route('/users/<user_id>')
def show_user_profile(user_id):
    """Show user specific profile"""

    user = crud.get_users_by_id(user_id)

    return render_template('user_profile.html', user=user)

@app.route('/users', methods = ['POST'])
def make_account():
    """Make account for new users"""

    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)

    if user:
        flash('This account already exists')
    else:
        new_user = crud.create_user(email = email,
        password = password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account was successfully created')
    
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login_to_account():
    """login into account"""

    email = request.form.get('email')
    password = request.form.get('password')
    user = crud.get_user_by_email(email)

    if user and user.password == password:
        session['user_id'] = user.user_id

### check password matching after email comes back as in db, then login
    if session.get('user_id'):
        flash('You have successfully logged in')
    else:
         flash('Check that your account name and password is correct or create an account above')

    return redirect('/')


@app.route('/movie/<movie_id>/rate')
def rate_a_movie(movie_id):
    """Rate a movie"""

    user_id = session['user_id']
    score = int(request.args.get("rate"))

    rating = Rating(user_id = user_id, 
    movie_id=movie_id, 
    score=score)

    db.session.add(rating)
    db.session.commit()

    return render_template('rating.html', rating=rating)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
