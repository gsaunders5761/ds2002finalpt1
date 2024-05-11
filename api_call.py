# DS 2002 Final Project Pt 2
# Grace Saunders and Anagha Chundhury

import requests
import sqlite3
import time

# fetch data from API
def fetch_data():
    url = "https://4feaquhyai.execute-api.us-east-1.amazonaws.com/api/pi"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data from API")
        return None

# create new SQLite3 database and table
def create_database_table():
    try:
        # connect to SQLite database
        connection = sqlite3.connect('api_data.db')
        cursor = connection.cursor()

        # create a table
        cursor.execute('''
            DROP TABLE IF EXISTS api_data
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_data (
                factor INTEGER PRIMARY KEY,
                pi INTEGER,
                time STRING
            )
        ''')
        connection.commit()
        print("Database and table successfully created")

    except sqlite3.Error as error:
        print("Error while creating database and table:", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("SQLite connection closed")

# store data in SQLite3 database
def store_data_in_database(data):
    try:
        # Connect to database
        connection = sqlite3.connect('api_data.db')
        cursor = connection.cursor()

        # Insert data into table
        insert_query = "INSERT INTO api_data (factor, pi, time) VALUES (?, ?, ?)"
        cursor.execute(insert_query, (data['factor'], data['pi'], data['time']))

        connection.commit()
        print("Data inserted")

    except sqlite3.Error as error:
        print("Error while inserting data into database:", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("SQLite connection closed")

# Main function to create table and execute the API call + table insert every minute
def main():
    create_database_table()

    # Run for 60 minutes
    for _ in range(60):
        data = fetch_data()
        if data:
            store_data_in_database(data)
        # Wait for one minute before making the next API call
        time.sleep(60)
if __name__ == '__main__':
    main()

# each time, the API returns pi rounded slightly differently after the first 3 digits.
# this is likely because pi is irrational, so it returns a slightly different variation each time
# the factor variable represents the cube (^3) of the number of times that the API has been called
# if you take the cube root of the factor column, it increases by 1 each time
# the time variable logs the time of each API call since the beginning of the process,
# increasing by about 1 minute each time

# Some calls threw an error during data insertion because the unique constraint failed for the factor variable
# which I set as the primary key during table creation, so I believe that may be why