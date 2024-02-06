import os
import psycopg2
import logging
import pandas as pd
import pyarrow
from netflix_rec_system.exceptions import (ConnectToDatabaseError, CreateTableError, DataValidationError, InsertError,
                                           FileNotFound)
from dotenv import load_dotenv

load_dotenv()
datas = "cleaned_movie_data.csv"


class DBUtility:
    def __init__(self) -> None:
        self.db_user = os.environ.get("DB_USER")
        self.db_password = os.environ.get("DB_PASSWORD")
        self.db_name = os.environ.get("DB_NAME")
        self.host = os.environ.get("HOST")
        self.port = os.environ.get("PORT")
        self.connection = None
        self.df = None

    def read_data(self, data) -> None:
        """
        This is used to read data from the csv file
        :return:
        """
        try:
            self.df = pd.read_csv(data)
            logging.info("Data loaded successfully")
        except Exception as e:
            raise FileNotFound("Csv file not found in specified path") from e

    def connect_to_database(self) -> None:
        """
        This function creates a connection to the database
        """
        try:
            self.connection = psycopg2.connect(
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_password,
                host=self.host,
                port=self.port
            )
            logging.info("connected to postgres database successfully")

        except Exception as e:
            raise ConnectToDatabaseError("cannot connect to postgres database") from e

    def create_postgres_table(self) -> None:
        """
        This function creates the postgresql table if it does not exist in the database
        """
        query = """
        CREATE TABLE IF NOT EXISTS movies (
        id SERIAL PRIMARY KEY,
        movie_id INTEGER,
        title VARCHAR(150) NOT NULL,
        year INTEGER,
        rated VARCHAR(10),
        runtime VARCHAR(10),
        genre VARCHAR(200),
        director VARCHAR(100),
        actors VARCHAR(200),
        plot VARCHAR(250),
        poster VARCHAR(250),
        language VARCHAR(200),
        country VARCHAR(200),
        imdb_rating FLOAT,
        user_id INTEGER,
        ratings FLOAT,
        type VARCHAR(50)
        )
        """

        try:
            # create cursor object
            cursor = self.connection.cursor()

            # execute raw query
            cursor.execute(query)

            # Commit the changes
            self.connection.commit()

            # Close the cursor object
            cursor.close()

            logging.info("table created successfully")
        except Exception as e:
            raise CreateTableError("cannot create table") from e

    def data_type_validation(self) -> None:
        for num in range(len(self.df)):
            data_types = {
                'movieId': int,
                'Title': str,
                'Year': int,
                'Rated': str,
                'Runtime': str,
                'Director': str,
                'Actors': str,
                'Plot': str,
                'Poster': str,
                'Language': str,
                'Country': str,
                'imdbRating': float,
                'Type': str,
                'Genre': str,
                'userId': int,
                'rating': float
            }
            # self.df['movieId'][0] = int(self.df['movieId'][0])
            if all(isinstance(self.df[col][num], data_type) for col, data_type in data_types.items()):
                logging.info('Data type validated')
            else:
                logging.info(f'Failed in {self.df.iloc[num]}')
                raise DataValidationError('Data type validation failed')

    def insert(self) -> None:
        """
        This function ingests the data into the database
        """
        for num in range(len(self.df)):
            try:
                insert_script = ("INSERT INTO movies (movie_id, title, year, rated, runtime, genre, director, actors, "
                                 "plot, poster, language, country, imdb_rating,user_id, ratings, type) "
                                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                insert_values = (f"{self.df['movieId'][num]}", f"{self.df['Title'][num]}",
                                 f"{self.df['Year'][num]}", f"{self.df['Rated'][num]}", f"{self.df['Runtime'][num]}",
                                 f"{self.df['Genres'][num]}", f"{self.df['Director'][num]}",
                                 f"{self.df['Actors'][num]}",
                                 f"{self.df['Plot'][num]}", f"{self.df['Poster'][num]}", f"{self.df['Language'][num]}",
                                 f"{self.df['Country'][num]}", f"{self.df['imdbRating'][num]}",
                                 f"{self.df['userId'][num]}",
                                 f"{self.df['rating'][num]}", f"{self.df['Type'][num]}")
                # create cursor object
                cursor = self.connection.cursor()
                if (self.df['movieId'][num] is not None or
                        self.df['Title'][num] is not None or
                        self.df['Year'][num] is not None or
                        self.df['Rated'][num] is not None or
                        self.df['Runtime'][num] is not None or
                        self.df['Director'][num] is not None or
                        self.df['Actors'][num] is not None or
                        self.df['Plot'][num] is not None or
                        self.df['Poster'][num] is not None or
                        self.df['Language'][num] is not None or
                        self.df['Country'][num] is not None or
                        self.df['imdbRating'][num] is not None or
                        self.df['Type'][num] is not None or
                        self.df['Genres'][num] is not None or
                        self.df['userId'][num] is not None or
                        self.df['rating'][num] is not None):
                    # execute raw query
                    cursor.execute(insert_script, insert_values)
                else:
                    logging.info("No input detected")

                # Commit the changes
                self.connection.commit()

                # Close the cursor object
                cursor.close()

                logging.info("Insert successful")
            except Exception as e:
                raise InsertError("cannot insert into table") from e


if __name__ == "__main__":
    db = DBUtility()
    db.read_data(datas)
    db.connect_to_database()
    db.create_postgres_table()
    db.data_type_validation()
    db.insert()
