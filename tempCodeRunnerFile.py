import requests
import mysql.connector

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="4444",
    database="IFootball"
)

# Create a cursor to interact with the database
cursor = db.cursor()

# Query to retrieve team_name and crest from the 'teams' table
query = "SELECT team_name, crest FROM teams"
cursor.execute(query)

# Fetch all rows from the query result
teams = cursor.fetchall()

def download_crest(team_name, crest_url):
    try:
        # Send a request to download the image
        response = requests.get(crest_url)
        response.raise_for_status()  # Check for HTTP errors

        # Define the filename (sanitize the team name to avoid issues)
        filename = f"crests/{team_name.replace(' ', '_').replace('/', '_')}.png"

        # Save the image
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {team_name}: {e}")

# Iterate over the rows and download each crest
for team_name, crest_url in teams:
    download_crest(team_name, crest_url)

# Close the cursor and database connection
cursor.close()
db.close()
