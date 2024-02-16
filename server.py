# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from flask import Flask, render_template, request
from app import genre, search_movie, director, user_rating

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

@app.route('/login',methods=['POST','GET'])
def login_credential():
    if request.method == 'POST':
        userId = request.form[]


@app.route('/search', methods=['POST'])
def search_page():
    if request.method == 'POST':
        movies = request.form['movie']
        movie = search_movie(movies)
        sug = suggestions(movie)
        direct = director(movie)
        user = user_rating(movie)
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
                               suggestion6=direct[0][2],
                               image_link6=direct[0][10],
                               description6=direct[0][9],
                               suggestion7=direct[1][2],
                               image_link7=direct[1][10],
                               description7=direct[1][9],
                               suggestion8=direct[2][2],
                               image_link8=direct[2][10],
                               description8=direct[2][9],
                               suggestion11=user[0][2],
                               image_link11=user[0][10],
                               description11=user[0][9],
                               suggestion12=user[1][2],
                               image_link12=user[1][10],
                               description12=user[1][9],
                               suggestion13=user[2][2],
                               image_link13=user[2][10],
                               description13=user[2][9],
                               suggestion14=user[3][2],
                               image_link14=user[3][10],
                               description14=user[3][9],
                               suggestion15=user[4][2],
                               image_link15=user[4][10],
                               description15=user[4][9])


# @app.route('/NotFound', methods=['POST'])
# def invalid():


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)
