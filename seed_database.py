"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())

movies_in_db = []

for movie in movie_data:
    title = movie['title']
    overview = movie['overview']
    poster_path = movie['poster_path']
    release_date = movie['release_date']
    format = '%Y-%m-%d'

    # can combine the release date steps into one line
    release_date = datetime.strptime(release_date, format)

    movie = crud.create_movie(
        title=title, 
        overview=overview, 
        release_date=release_date, 
        poster_path=poster_path
    )
    
    movies_in_db.append(movie)

model.db.session.add_all(movies_in_db)
model.db.session.commit()


for n in range(10):
    email = f'user{n}@test.com' 
    password = 'test'

    test_user = crud.create_user(email, password)
    
    model.db.session.add(test_user)

    for _ in range(10):
        rating = crud.create_rating(score =  randint(0, 5), 
        movie = choice(movies_in_db),
        user = test_user)

        model.db.session.add(rating)

model.db.session.commit()

