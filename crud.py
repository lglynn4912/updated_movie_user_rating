"""CRUD operations."""


from model import db, User, Movie, Rating, connect_to_db

def create_movie(title, overview, release_date, poster_path):
    """Create and return information about a movie."""

    return Movie(title=title, overview=overview,
    release_date=release_date, poster_path=poster_path)


def get_movies(): 
    "returns all movies"

    return Movie.query.all()


def get_movies_by_id(movie_id):
    "return info about move from movie id"
    
    return Movie.query.get(movie_id)
    

def create_user(email, password):
    """Create and return a new user."""

    return User(email=email, password=password)


def get_users(): 
    """returns all users"""

    return User.query.all()


def get_users_by_id(user_id): 
    """Returns user information by id"""

    return User.query.get(user_id)


def get_user_by_email(email):

    return User.query.filter_by(email=email).first()


def create_rating(user, movie, score):

    return Rating(user = user, movie = movie, score = score)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)