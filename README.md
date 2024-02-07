This Repo Contains Project Done as Volunteer Research Assistant at Northeastern University, Boston for the Dept of Mechanical and Industrial Engineering.

This project will create a data pipeline to retrieve weather data from a free weather API, process it, and store it in a database after analysis.

Components:

1. API Client: Python script to call the weather API and fetch data.
2. Data Processing: Clean and format the retrieved data.
3. Database Storage: Store the processed data in a database (SQLite).
4. Scheduler: Automate data retrieval at regular intervals.


Implementation : 

1. API Client (fetch_weather_data): This function fetches weather data for multiple cities using the OpenWeatherMap API. It takes an API key and a list of cities as input and returns a list of weather data for each city.

2. Database Storage (create_connection, create_table, insert_data): These functions handle database operations using SQLite. They create a database connection, create a table to store weather data if it doesn't exist, and insert weather data into the database.

3. Analysis (analyze_weather_data): This function performs analysis on the collected weather data. It calculates the average temperature and humidity for each city and prints the results.

4. Main Script (__main__): This part of the script initializes variables, establishes a connection to the database, and orchestrates the data collection, storage, and analysis processes. It continuously fetches weather data at regular intervals using the API client, stores it in the database, and analyzes the collected data.
