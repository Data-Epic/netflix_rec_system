# pylint: disable=missing-module-docstring
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_name = os.environ.get("DB_NAME")
host = os.environ.get("HOST")
port = os.environ.get("PORT")

con = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_password,
    host=host,
    port=port)

cursor = con.cursor()


def search_movie(movie_name):
    """
    This function is used to search for movies in the database
    :param movie_name: This expects the name of desired movie
    :return:
    """
    cursor.execute(f"SELECT * FROM movies WHERE title ~ '\m{movie_name.title()}'")
    columns = []
    for column in cursor.description:
        columns.append(column[0].lower())
    movies = {}
    for row in cursor:
        for i in range(len(row)):
            movies[columns[i]] = row[i]
            if isinstance(row[i], str):
                movies[columns[i]] = row[i].strip()
    return movies


def suggestions(movies):
    """
    This function is used to generate suggestions based on similar genres
    :param movies: This expects a dict of movie details
    :return:
    """
    cursor.execute(f"SELECT * FROM movies WHERE genre = "
                   f"'{movies['genre']}' ORDER BY random() LIMIT 5")
    columns = []
    for column in cursor.description:
        columns.append(column[0].lower())
    movies1 = []
    for row in cursor:
        movies1.append(row)
    return movies1


def random_movies():
    """
    This function is used to generate random movies from the database
    :return:
    """
    cursor.execute("SELECT * FROM movies WHERE ratings > 2.5 ORDER BY random() LIMIT 5")
    columns = []
    for column in cursor.description:
        columns.append(column[0].lower())
    random = []
    for row in cursor:
        random.append(row)
    return random


def director(movies):
    """
    This function is used to generate suggestions based on the director
    :param movies: This expects a dict of movie details
    :return:
    """
    cursor.execute(f"SELECT * FROM movies WHERE director = '{movies['director']}' ORDER BY random() LIMIT 5")
    columns = []
    for column in cursor.description:
        columns.append(column[0].lower())
    movies1 = []
    for row in cursor:
        movies1.append(row)
    return movies1


def user_rating(movies):
    """
    This function is used to generate suggestions based on similar user ratings
    :param movies: This expects a dict of movie details
    :return:
    """
    cursor.execute(f"SELECT * FROM movies WHERE ratings > '{movies['ratings']}' ORDER BY random() LIMIT 5")
    columns = []
    for column in cursor.description:
        columns.append(column[0].lower())
    movies1 = []
    for row in cursor:
        movies1.append(row)
    return movies1


# movie = search_movie('avenger')
# sug = suggestions(movie)
# rand = random_movies()
# print(movie)
# print(sug)
# print(rand[0])
# print(rand[1])
# print(rand[2])
# print(rand[3])
# print(rand[4])
