# Netflix Recommendation System

## Overview
Our CEO, Jian Yiang, wants us to create a movie recommendation system that suggests movies to users based on their preferences. This system is the first of its kind and has no resemblance to any other product whatsoever.

In this project, we used multiple scripts.

The provided script in `database_connection.py` defines a utility class, `DBUtility`, for connection to the database using psycopg2 and also performing other functions such as creation of table, data type validation and insertion of data  

The `DBUtility` class contains the following methods:

- `read_data`: Extracts `movie` data from a a csv file.
- `connect_to_database`: Connects to a PostgreSQL render database.
- `create_postgres_table`: Creates a PostgreSQL table named `movies` with specific columns.
- `data_type_validation`:  Applies CHECK to ensure specific data types are met
- `insert`: Inserts data into the `movies` table from the extracted DataFrame.

The provided script in `app.py` is used for interacting with the database saved data.

The `app.py` contains the following methods

- `search_movie`: This function extracts a specific title from the database based on user input.
- `genre`: This function produces suggestions based on similar genre of the movie searched for by the user.
- `random_movies`: This function generates random movies from the database where user rating is greater than 2.5.
- `director`: This function produces suggestions based on similar director of the movie searched for by the user.
- user_ration: This function generates suggestions based on similar user rating of the user input. 

The provided script in `server.py` is used for the deployment of the flask server.

### Data source:
For the data we used,we gathered data from the movielens api then transferred its information into another api called omdb api, which is used for generating adequate details about movies.

## Technologies used
- Bash
- Flask
- PostgreSQL
- Python  <br>
  *Dependencies used:*
  - pandas: `^2.1.3`
  - psycopg2-binary: `^2.9.9`
  - python-dotenv: `^1.0.0`
  - flask: `^3.0.2`
  - pytest: `^8.0.0`
  - requests: `^3.21.0`


## Prerequisites
- Cloud-based database server such as Render
- PotgresSQL Database on render 
- Python3.9+ Intepreter
- Poetry `^1.7.1`
- Flask `^3.0.2`

## Project build & setup 
___
- **setup development environment:** 
  - `poetry env use python3.11` 
  - `poetry install` 
<br>

- **Create dedicated database**

  - login to render to create the database details 
 
  - create a new user
  - 
  - create a new database

  - grant user privileges on a new database

<br>

- **Create and define required env variables in the `.env` file**
  
      
      DB_USER=<"your_db_username>
      DB_PASSWORD=<"your_db_password>
      DB_NAME=<"your_database_name">
      HOST=<"render_hostname">
      PORT="5432"

- **run `database_connection.py` script from entry point with `poetry`**: `poetry run python database_connection.py` 

### Project Directory structure
      netflix_rec_system
      .
      ├── app.py
      ├── cleaned_movie_data.csv
      ├── exceptions.py
      ├── server.py
      ├── poetry.lock
      ├── pyproject.toml
      ├── Movie Recommender Systems.docx
      ├── static
      │   └── style.css
      ├── templates
      │    └── index.html
      │        search.html
      ├── analysis_notebook
      │    └── Analysis new_netflix.ipynb
      ├── cleaning_notebook
      │    └── Cleaning Movie Recommender.ipynb
      ├── model_building
      │    └── model_new_netflix.ipynb
      ├──tests
      │    └── test_database_connection.py
      └── README.md

- `app.py`: Interaction with the database
- `exceptions.py`: all error exception handling happens here
- `server.py`: flask server script exists here
- `database_connection.py`: Database connection scripts exist here
- `poetry.lock`: lock file for dependencies (recomended over toml file for installation)
- `pyproject.toml`: poetry project dependencies and meta-data

## Results
