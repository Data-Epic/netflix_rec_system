# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from joblib import load
import sys
import os
from flask import Flask, render_template, request
SCRIPT_DIR = os.path.dirname(os.path.abspath('apps.py'))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from model_building.model_classes import MatrixFactorization, ContentBased, HybridRecommender, movie_data_comb1, train_df
from netflix_rec_system.apps import (genre, search_movie, director, user_rating, random_movies, get_movies,
                                     search_suggestion, search_recommendation, recommend_movies)

app = Flask(__name__)


@app.route('/')
def open_app():
    movie = random_movies()
    return render_template('index.html',
                           title1=movie[0][2],
                           description1=movie[0][9],
                           image_link=movie[0][10],
                           title2=movie[1][2],
                           description2=movie[1][9],
                           image_link1=movie[1][10],
                           title3=movie[2][2],
                           description3=movie[2][9],
                           image_link3=movie[2][10],
                           title4=movie[3][2],
                           description4=movie[3][9],
                           image_link4=movie[3][10],
                           title5=movie[4][2],
                           description5=movie[4][9],
                           image_link5=movie[4][10])


@app.route('/server')
def login_page():
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def login_credential():
    if request.method == 'POST':
        userid = request.form['userId']
        movies_liked = request.form['movies']
        move = search_movie(movies_liked)
        movie_list = recommend_movies(userid, move['title'])
        movies = get_movies(movie_list)
    return render_template('user.html',
                           userId=userid,
                           suggestion1=movies[0][2],
                           image_link1=movies[0][10],
                           description1=movies[0][9],
                           suggestion2=movies[1][2],
                           image_link2=movies[1][10],
                           description2=movies[1][9],
                           suggestion3=movies[2][2],
                           image_link3=movies[2][10],
                           description3=movies[2][9],
                           suggestion4=movies[3][2],
                           image_link4=movies[3][10],
                           description4=movies[3][9],
                           suggestion5=movies[4][2],
                           image_link5=movies[4][10],
                           description5=movies[4][9]
        )


@app.route('/search', methods=['POST'])
def search_page():
    if request.method == 'POST':
        movies = request.form['movie']
        movie = search_movie(movies)
        move = search_suggestion(movie['title'])
        sug = get_movies(move)
        return render_template('search.html',
                               title=movie['title'],
                               image_link=movie['poster'],
                               description=movie['plot'],
                               suggestion1=sug[0][2],
                               image_link1=sug[0][10],
                               description1=sug[0][9],
                               suggestion2=sug[1][2],
                               image_link2=sug[1][10],
                               description2=sug[1][9],
                               suggestion3=sug[2][2],
                               image_link3=sug[2][10],
                               description3=sug[2][9],
                               suggestion4=sug[3][2],
                               image_link4=sug[3][10],
                               description4=sug[3][9],
                               suggestion5=sug[4][2],
                               image_link5=sug[4][10],
                               description5=sug[4][9],
                               suggestion6=sug[5][2],
                               image_link6=sug[5][10],
                               description6=sug[5][9],
                               suggestion7=sug[6][2],
                               image_link7=sug[6][10],
                               description7=sug[6][9],
                               suggestion8=sug[7][2],
                               image_link8=sug[7][10],
                               description8=sug[7][9],
                               suggestion9=sug[8][2],
                               image_link9=sug[8][10],
                               description9=sug[8][9],
                               suggestion10=sug[9][2],
                               image_link10=sug[9][10],
                               description10=sug[9][9]
                               )


@app.route('/NotFound', methods=['POST'])
def invalid():
    pass


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
