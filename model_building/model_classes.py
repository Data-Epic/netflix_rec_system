import pandas as pd
import numpy as np
from sklearn.base import RegressorMixin, BaseEstimator
from joblib import load
import matplotlib.pyplot as plt

movie_data_comb1 = pd.read_csv("cleaned_movie_data.csv")
user_id = 9
movie_user_likes='v for vendetta'
train_df = movie_data_comb1.drop(columns=['userId','rating']).drop_duplicates().reset_index(drop=True)
train_df['Title'] = train_df['Title'].apply(lambda x: x.lower())

class MatrixFactorization(BaseEstimator, RegressorMixin):
    k = 20
    n_users = movie_data_comb1['userId'].nunique()
    n_movies = movie_data_comb1['movieId'].nunique()
    R = movie_data_comb1.pivot_table(index='userId', columns='movieId', values='rating').fillna(0).to_numpy()
    P = np.random.normal(scale=1. / k, size=(n_users, k))
    Q = np.random.normal(scale=1. / k, size=(n_movies, k))

    def __init__(self, alpha=0.01, beta=0.01, iterations=100):
        self.beta = beta
        self.alpha = alpha
        self.iterations = iterations
        self.predictions_df = pd.DataFrame()
        self.errors_ = []
        self.iterations_ = []

    def fit(self):
        for i in range(self.iterations):
            for u in range(self.n_users):
                for m in range(self.n_movies):
                    if self.R[u, m] > 0:
                        pred = np.dot(self.P[u, :], self.Q[m, :].T)
                        error = self.R[u, m] - pred
                        self.P[u, :] = self.P[u, :] + self.alpha * (error * self.Q[m, :] - self.beta * self.P[u, :])
                        self.Q[m, :] = self.Q[m, :] + self.alpha * (error * self.P[u, :] - self.beta * self.Q[m, :])
            error = 0
            for u in range(self.n_users):
                for m in range(self.n_movies):
                    if self.R[u, m] > 0:
                        error += (self.R[u, m] - np.dot(self.P[u, :], self.Q[m, :].T)) ** 2
                        error += (self.beta / 2) * (
                                    np.linalg.norm(self.P[u, :]) ** 2 + np.linalg.norm(self.Q[m, :]) ** 2)
            if (i + 1) % 10 == 0:
                print(f'Iteration: {i + 1}, error: {error}')
                self.errors_.append(error)
                self.iterations_.append(i)

        predictions = np.dot(self.P, self.Q.T)

        self.predictions_df = pd.DataFrame(predictions,
                                           columns=movie_data_comb1.pivot_table(index='userId', columns='movieId',
                                                                                values='rating').fillna(0).columns,
                                           index=movie_data_comb1.pivot_table(index='userId', columns='movieId',
                                                                              values='rating').fillna(0).index)

    def plot_curve(self):
        plt.figure(figsize=(13, 10))
        plt.plot(self.iterations_, self.errors_)
        plt.xlabel("Iterations")
        plt.ylabel("Errors")
        plt.show()

    def get_title_from_index(self, df, id):
        return df[df.movieId == id]['Title'].values[0]

    def get_index_from_title(self, df, title):
        return df[df.Title == title].index.values[0]

    def predict(self, userId, n=5):

        if userId not in movie_data_comb1['userId'].unique():
            return ('Sorry! The user is not in our database. Try Popularity based')

        user_ratings = movie_data_comb1[movie_data_comb1['userId'] == userId]
        user_predictions = self.predictions_df.loc[userId]
        user_predictions = user_predictions[~user_predictions.index.isin(user_ratings['movieId'])]
        user_predictions = user_predictions.sort_values(ascending=False)
        user_predictions = user_predictions.head(n)
        predictions = []
        for movie in user_predictions.index.values:
            #     if get_title_from_index(train,movie) == movie_user_likes:
            #         continue
            predictions.append(self.get_title_from_index(movie_data_comb1, movie))
        # print(movie)
        return predictions


# collaborative_model = load("collaborative_model.joblib")
# print(collaborative_model.predict(9,10))


#Content Based
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentBased(BaseEstimator):
    def __init__(self):
        self.similarity = np.empty(0)

    def get_title_from_index_(self, df, index):
        return df[df.index == index]['Title'].values[0]

    def get_index_from_title_(self, df, title):
        return df[df.Title == title].index.values[0]

    def fit(self):
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(train_df['comb'])
        self.similarity = cosine_similarity(count_matrix)

    def predict(self, movie_user_likes):

        if movie_user_likes not in train_df['Title'].unique():
            return (
                'Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies')

        movie_index = self.get_index_from_title_(train_df, movie_user_likes)
        similar_movies = list(enumerate(self.similarity[movie_index]))
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)
        i = 0
        recommend = []
        for movie in sorted_similar_movies:
            if self.get_title_from_index_(train_df, movie[0]) == movie_user_likes:
                continue
            recommend.append(self.get_title_from_index_(train_df, movie[0]))
            i += 1
            if i == 10:
                break
        return recommend

# content_model = load("content_model.joblib")
# print(f"content reco:{content_model.predict('v for vendetta')}")
# # #Hybrid
class HybridRecommender:
    def __init__(self, content_model, collaborative_model, content_weight=0.5):
        self.content_model = content_model
        self.collaborative_model = collaborative_model
        self.content_weight = content_weight

    def recommend(self, user_id, movie_user_likes, n=5):
        if (user_id in movie_data_comb1['userId'].unique()) and (movie_user_likes in train_df['Title'].unique()):
            content_recommendations = self.content_model.predict(movie_user_likes)
            collaborative_recommendations = self.collaborative_model.predict(user_id, n)

            hybrid_recommendations = self.combine_recommendations(content_recommendations, collaborative_recommendations)
            return hybrid_recommendations
        else:
            popularity_recommend = self.popularity_recommendations()
            return popularity_recommend

    def combine_recommendations(self, content_recommendations, collaborative_recommendations,n=5):
        num_content_recommendations = len(content_recommendations)
        num_collaborative_recommendations = len(collaborative_recommendations)

        num_content_to_take = int(n * self.content_weight)
        num_collaborative_to_take = n - num_content_to_take
        combined_recommendations = (content_recommendations[:num_content_to_take] +
                                    collaborative_recommendations[:num_collaborative_to_take])
        return combined_recommendations

    def popularity_recommendations(self,n=5):
        if n > len(movie_data_comb1.loc[(movie_data_comb1['rating']==4) | (movie_data_comb1['rating']==5),
                     ['Title','rating']]):
            return "not enough movie in database"

        popularity_recommend = movie_data_comb1.loc[(movie_data_comb1['rating']==4) | (movie_data_comb1['rating']==5),
                     ['Title','rating']].sort_values(by=['rating'],ascending=False)['Title'].values[:5]
        return popularity_recommend

# hybrid_recommender = HybridRecommender(content_model, collaborative_model)
#
#
# print(f"hybrid: {hybrid_recommender.recommend(user_id, movie_user_likes)}")