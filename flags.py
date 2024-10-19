import os
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

# Query to retrieve team_id, team_name, and crest from the 'teams' table
query = "SELECT team_id, team_name, crest FROM teams"
cursor.execute(query)

# Fetch all rows from the query result
teams = cursor.fetchall()

# Use absolute paths to avoid issues with relative paths
current_dir = os.path.dirname(os.path.abspath(__file__))
crests_dir = os.path.join(current_dir, 'IFootball\crests')

# Create the 'crests' directory if it doesn't exist
if not os.path.exists(crests_dir):
    try:
        os.makedirs(crests_dir, exist_ok=True)
        print(f"Directory created: {crests_dir}")
    except Exception as e:
        print(f"Error creating directory: {e}")
        exit(1)

def download_crest(team_id, crest_url):
    try:
        # Download the image using requests
        response = requests.get(crest_url)
        response.raise_for_status()  # Check for HTTP errors

        # Use team_id for the filename
        filename = os.path.join(crests_dir, f"{team_id}.png")

        # Save the image
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download crest for team ID {team_id}: {e}")

    except FileNotFoundError as e:
        print(f"File error: {e}")

# Iterate over the teams and download each crest
for team_id, team_name, crest_url in teams:
    download_crest(team_id, crest_url)

# Close the cursor and database connection
cursor.close()
db.close()
