import os
import pytest
import pandas as pd
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath('database_connection.py'))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from netflix_rec_system.database_connection import (DBUtility, FileNotFound, DataValidationError, InsertError)


@pytest.fixture
def db_utility():
    return DBUtility()


def test_read_data_csv_exists(db_utility, tmp_path):
    # Create a temporary CSV file for testing
    test_data = pd.DataFrame({'movieId': [1, 2, 3], 'Title': ['Movie1', 'Movie2', 'Movie3'],
                              'Year': ['2020', '2021', '2022']})
    csv_path = tmp_path / 'test_data.csv'
    test_data.to_csv(csv_path, index=False)

    # Test reading data from the created CSV file
    db_utility.read_data(csv_path)

    # Assert that the data is loaded successfully
    assert db_utility.df is not None
    assert not db_utility.df.empty


def test_read_data_csv_not_exists(db_utility):
    # Test handling the case where the CSV file does not exist
    with pytest.raises(FileNotFound):
        db_utility.read_data("nonexistent_file.csv")


def test_connect_to_database(db_utility):
    # Test connecting to the database
    db_utility.connect_to_database()

    # Assert that the connection is not None
    assert db_utility.connection is not None


def test_create_postgres_table(db_utility):
    # Test creating the PostgreSQL table
    db_utility.connect_to_database()
    db_utility.create_postgres_table()


def test_data_type_validation(db_utility):
    # # Set up a DataFrame with incorrect data types for testing
    test_data = pd.DataFrame({'movieId': ['August', 'january', 'may'], 'Title': [1, 2, 3],
                              'Genres': [1, '1', 3], 'Year': ['2020', '2021', '2022'],
                              'Rated': [1, 2, 4], 'Runtime': [120, 150, 90],
                              'Director': [1, 2, 4],
                              })

    # # Assign the DataFrame to the DBUtility instance
    db_utility.df = test_data
    # db_utility.data_type_validation()
    # Test data type validation
    with pytest.raises(DataValidationError, match='Data type validation failed'):
        db_utility.data_type_validation()


def test_insert(db_utility):
    # Set up a DataFrame for testing
    test_data = pd.DataFrame({'movieId': [1, 2, 3], 'Title': ['Movie1', 'Movie2', 'Movie3'],
                              'Genres': ['Action', 'Drama', 'Comedy'], 'Year': [2020, 2021, 2022],
                              'Rated': ['PG', 'R', 'PG-13'], 'Runtime': ['120 min', '150 min', '90 min'],
                              # 'Director': ['Director1', 'Director2', 'Director3'],
                              'Actors': ['Actor1, Actor2', 'Actor3, Actor4', None],
                              'Plot': ['Plot1', 'Plot2', 'Plot3'],
                              'Poster': ['poster1.jpg', 'poster2.jpg', 'poster3.jpg'],
                              'Language': ['English', 'Spanish', 'French'],
                              'Country': ['USA', 'Spain', 'France'],
                              'imdbRating': [8.0, 7.5, 6.5],
                              'userId': [101, 102, 103],
                              'rating': [4.5, 3.5, 5.0],
                              'Type': ['Movie', 'TV Show', 'Movie']})

    # Assign the DataFrame to the DBUtility instance
    db_utility.df = test_data
    # Test inserting data into the database
    with pytest.raises(InsertError):
        db_utility.insert()


