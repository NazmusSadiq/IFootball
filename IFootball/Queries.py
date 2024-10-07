import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="210041139",
    database="IFootball"
)
cursor = db.cursor()

class Queries:
    
    def fetch_teams_from_database():
        try:
            # Execute the query to get team names from the database
            cursor.execute("SELECT team_name FROM teams")

            # Fetch all team names and return them as a list
            teams = [row[0] for row in cursor.fetchall()]
            return teams
        except Exception as e:
            print(f"Error fetching teams from database: {e}")
            return []
