# pylint: disable=missing-module-docstring
import os
import sys

import psycopg2
from dotenv import load_dotenv
from joblib import load

SCRIPT_DIR = os.path.dirname(os.path.abspath('model_building/model_classes.py'))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from model_building.model_classes import (ContentBased, MatrixFactorization, HybridRecommender,
                                          movie_data_comb1, train_df)

load_dotenv()
file_path = os.path.join("model_building", "content_model.joblib")
content_model = load(file_path)
file_paths = os.path.join("model_building", "collaborative_model.joblib")
collaborative_model = load(file_paths)
hybrid_recommender = HybridRecommender(content_model, collaborative_model)

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
                movies[columns[i]] = row[i].strip().lower()
    return movies


def search_suggestion(movie_name):
    movied = content_model.predict(movie_name)
    return movied


def recommend_movies(userId, movies_liked):
    movie_list = hybrid_recommender.recommend(userId, movies_liked)
    return movie_list


def genre(movies):
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

def search_recommendation(movie_list):
    """
    This function is used to generate random movies from the database
    :return:
    """
    random = []
    columns = []
    for movies in movie_list:
        movies = movies.lower()
        id_ = train_df.loc[train_df['Title'] == movies, 'movieId'].values[0]
        movies = movie_data_comb1.loc[movie_data_comb1['movieId'] == id_, 'Title'].values[0]
        query = "SELECT * FROM movies WHERE title = %s LIMIT 1"
        cursor.execute(query, (movies,))
        for column in cursor.description:
            columns.append(column[0].lower())
        for row in cursor:
            random.append(row)
    return random


def get_movies(movie_list):
    """
    This function is used to generate random movies from the database
    :return:
    """
    random = []
    columns = []
    for movies in movie_list:
        movies = movies.lower()
        id_ = train_df.loc[train_df['Title'] == movies, 'movieId'].values[0]
        movies = movie_data_comb1.loc[movie_data_comb1['movieId'] == id_, 'Title'].values[0]
        query = "SELECT * FROM movies WHERE title= %s LIMIT 1"
        cursor.execute(query, (movies,))
        for column in cursor.description:
            columns.append(column[0].lower())
        for row in cursor:
            random.append(row)
    return random


def random_movies():
    random = []
    columns = []
    cursor.execute(f"SELECT * FROM movies ORDER BY random() LIMIT 5")
    for column in cursor.description:
        columns.append(column[0].lower())
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


# import os
# import psycopg2
# import pandas as pd
# from joblib import load
# from flask import Flask,request,render_template
# from model_building.model_classes import MatrixFactorization,ContentBased,HybridRecommender
#
#
# movie_data_comb1 = pd.read_csv("dataset/cleaned_movie_data.csv")
# train_df = movie_data_comb1.drop(columns=['userId','rating']).drop_duplicates().reset_index(drop=True)
# train_df['Title'] = train_df['Title'].apply(lambda x: x.lower())
# collaborative_model = load("model_building/collaborative_model.joblib")
# content_model = load("model_building/content_model.joblib")
# user_id = 9
# movie_user_likes='v for vendetta'
#
# hybrid_recommender = HybridRecommender(content_model, collaborative_model)
#
# print(f"collaborative: {collaborative_model.predict(9,10)}")
# print(f"content: {content_model.predict('v for vendetta')}")
# print(f"hybrid: {hybrid_recommender.recommend(user_id, movie_user_likes)}")


if __name__ == "__main__":
#     # movie_list = recommend_movies(9,"avatar", 10)
#     # print(len(get_movies(movie_list)))
    move = search_movie('pirate')
    print(move)
    movie = search_suggestion(move['title'])
    mov = get_movies(movie)
    print(mov)



