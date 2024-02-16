# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import os
import logging
import psycopg2
import numpy as np
import pandas as pd
import pyarrow
from dotenv import load_dotenv
from netflix_rec_system.exceptions import (ConnectToDatabaseError, CreateTableError, DataValidationError,
                        InsertError, FileNotFound)

load_dotenv()
DATA = "cleaned_movie_data.csv"
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
HOST = os.environ.get("HOST")
PORT = os.environ.get("PORT")

class DBUtility:
    def __init__(self) -> None:
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
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=HOST,
                port=PORT
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
        runtime INTEGER,
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
        """
        This function validated the data type.
        :return:
        """
        data_types = {
            'movieId': np.int64,
            'Title': str,
            'Year': np.int64,
            'Rated': str,
            'Runtime': np.int64,
            'Director': str,
            'Actors': str,
            'Plot': str,
            'Poster': str,
            'Language': str,
            'Country': str,
            'imdbRating': np.float64,
            'Type': str,
            'Genres': str,
            'userId': np.int64,
            'rating': np.float64
        }
        for num in range(len(self.df)):
            if all(isinstance(self.df[col][num], data_type) for col, data_type in data_types.items()):
                logging.info('Data type validated')
            else:
                # logging.info("Failed in %s", self.df.iloc[num])
                print(f"Failed in: \n{self.df.iloc[num]}")
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
                data_input = {
                    'movieId': None,
                    'Title': None,
                    'Year': None,
                    'Rated': None,
                    'Runtime': None,
                    'Director': None,
                    'Actors': None,
                    'Plot': None,
                    'Poster': None,
                    'Language': None,
                    'Country': None,
                    'imdbRating': None,
                    'Type': None,
                    'Genres': None,
                    'userId': None,
                    'rating': None
                }
                if all(isinstance(self.df[col][num] is not data) for col, data in data_input.items()):
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
    db.read_data(DATA)
    # db.connect_to_database()
    # db.create_postgres_table()
    db.data_type_validation()
    # db.insert()
