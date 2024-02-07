# -*- coding: utf-8 -*-
"""Script_For_Data_Collection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XlJaKxS234AQ1MSbEZp1nmwats6TP2nP
"""

import requests
import sqlite3
from datetime import datetime, timedelta
import time

# API Client - Fetch weather data for multiple cities
def fetch_weather_data(api_key, cities):
    weather_data_all_cities = []
    for city in cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            weather_data_all_cities.append(response.json())
        else:
            print(f"Failed to fetch data for {city}: {response.status_code}")
    return weather_data_all_cities

# Database Storage - Store weather data in the database
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

def create_table(conn):
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY,
        city TEXT NOT NULL,
        temperature REAL,
        humidity REAL,
        timestamp DATETIME
    );
    '''
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def insert_data(conn, data):
    sql = ''' INSERT INTO weather_data(city, temperature, humidity, timestamp)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid

# Analysis - Perform analysis on the collected data
def analyze_weather_data(conn):
    # Calculate average temperature and humidity for each city
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT city FROM weather_data")
    cities = cursor.fetchall()

    for city in cities:
        city_name = city[0]
        cursor.execute(f"SELECT AVG(temperature), AVG(humidity) FROM weather_data WHERE city='{city_name}'")
        result = cursor.fetchone()
        avg_temperature = result[0]
        avg_humidity = result[1]
        print(f"Average weather in {city_name}:")
        print(f"Average Temperature: {avg_temperature}°C")
        print(f"Average Humidity: {avg_humidity}%")
        print("")

if __name__ == "__main__":
    api_key = '4d0031a5ae2f0c28e3f8bed5939fabd0'
    us_cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio',
                 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'San Francisco', 'Indianapolis',
                 'Columbus', 'Fort Worth', 'Charlotte', 'Seattle', 'Denver', 'El Paso', 'Washington', 'Boston',
                 'Detroit', 'Nashville', 'Portland', 'Memphis', 'Oklahoma City', 'Las Vegas', 'Louisville',
                 'Baltimore', 'Milwaukee', 'Albuquerque', 'Tucson', 'Fresno', 'Mesa', 'Sacramento', 'Atlanta',
                 'Kansas City', 'Colorado Springs', 'Miami', 'Raleigh', 'Omaha', 'Long Beach', 'Virginia Beach',
                 'Oakland', 'Minneapolis', 'Tulsa', 'Tampa', 'Arlington']

    database = 'weather_data.db'
    conn = create_connection(database)
    if conn:
        create_table(conn)

        while True:
            weather_data_all_cities = fetch_weather_data(api_key, us_cities)

            if weather_data_all_cities:
                for weather_data in weather_data_all_cities:
                    city_name = weather_data['name']
                    temperature = weather_data['main']['temp']
                    humidity = weather_data['main']['humidity']
                    timestamp = datetime.now()

                    data_to_insert = (city_name, temperature, humidity, timestamp)
                    insert_data(conn, data_to_insert)

                print("Data successfully inserted into the database.")

                # Perform analysis on the collected data
                analyze_weather_data(conn)

            else:
                print("No weather data fetched. Check your API key or city names.")

            # Fetch data every 6 hours
            time.sleep(21600)  # Sleep for 6 hours (21600 seconds)

        conn.close()
    else:
        print("Failed to connect to the database.")