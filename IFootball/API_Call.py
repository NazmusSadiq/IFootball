
import mysql.connector
import requests
from datetime import datetime, timedelta

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="210041139",
    database="IFootball"
)
cursor = db.cursor()

# Check if there are any matches in the database
cursor.execute("SELECT COUNT(*) FROM matches")
match_count = cursor.fetchone()[0]

if match_count > 0: 
    cursor.execute("SELECT MAX(match_utc_date) FROM matches WHERE status = 'FINISHED'")
    result = cursor.fetchone()
    earliest_date = result[0]
    start_date = earliest_date.strftime('%Y-%m-%d')  # use last date for which database is updated
else:
    start_date = '2024-08-01'  # Use season start date
    
# API call to get data
API_TOKEN = '8511ddac058c4982b7c64722e71b77ee'
headers = {'X-Auth-Token': API_TOKEN}

# Get current date and add 2 weeks
end_date = (datetime.now() + timedelta(weeks=2)).strftime('%Y-%m-%d')


# Helper function to make API calls for a given date range
def fetch_matches_for_date_range(start, end):
    uri = f'https://api.football-data.org/v4/matches?dateFrom={start}&dateTo={end}'
    response = requests.get(uri, headers=headers)
    
    if response.status_code == 200:
        return response.json()['matches']
    else:
        print(f"Failed to fetch data from {start} to {end}. Status code: {response.status_code}")
        return []

# Break the date range into 10-day intervals and fetch data
def fetch_matches_in_intervals(start_date, end_date):
    current_start = datetime.strptime(start_date, '%Y-%m-%d')
    final_end = datetime.strptime(end_date, '%Y-%m-%d')
    all_matches = []

    while current_start <= final_end:
        current_end = current_start + timedelta(days=9)
        if current_end > final_end:
            current_end = final_end

        matches = fetch_matches_for_date_range(current_start.strftime('%Y-%m-%d'), current_end.strftime('%Y-%m-%d'))
        all_matches.extend(matches)

        current_start = current_end + timedelta(days=1)
    
    return all_matches

# Fetch all matches for the given month
matches = fetch_matches_in_intervals(start_date, end_date)

# Insert teams, seasons, competitions, and areas if they don't already exist
for match in matches:
    competition_id = match['competition']['id']
    
    # Check if competition_id is one of the specified values
    if competition_id in [2001, 2002, 2015, 2019, 2021, 2014]:        #top 5 leagues and UCL
        # Insert Area
        area = match['area']
        cursor.execute("""
            INSERT INTO areas (area_id, area_name, area_code, area_flag)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE area_name=VALUES(area_name), area_code=VALUES(area_code), area_flag=VALUES(area_flag)
        """, (area['id'], area['name'], area['code'], area['flag']))

        # Insert Home Team
        home_team = match['homeTeam']
        cursor.execute("""
            INSERT INTO teams (team_id, team_name, short_name, tla, crest)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE team_name=VALUES(team_name), short_name=VALUES(short_name), tla=VALUES(tla), crest=VALUES(crest)
        """, (home_team['id'], home_team['name'], home_team['shortName'], home_team['tla'], home_team['crest']))

        # Insert Away Team
        away_team = match['awayTeam']
        cursor.execute("""
            INSERT INTO teams (team_id, team_name, short_name, tla, crest)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE team_name=VALUES(team_name), short_name=VALUES(short_name), tla=VALUES(tla), crest=VALUES(crest)
        """, (away_team['id'], away_team['name'], away_team['shortName'], away_team['tla'], away_team['crest']))

        # Insert Season
        season = match['season']
        cursor.execute("""
            INSERT INTO seasons (season_id, start_date, end_date, current_matchday)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE start_date=VALUES(start_date), end_date=VALUES(end_date), current_matchday=VALUES(current_matchday)
        """, (season['id'], season['startDate'], season['endDate'], season['currentMatchday']))

        # Insert Competition
        competition = match['competition']

        # Check if the competition name is 'Primera Division' and replace it with 'LaLiga'
        competition_name = competition['name']
        if competition_name.lower() == 'primera division':
            competition_name = 'LaLiga'

        # Insert or update the competition in the database
        cursor.execute("""
            INSERT INTO competitions (competition_id, competition_name, competition_code, competition_type, competition_emblem)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE competition_name=VALUES(competition_name), competition_code=VALUES(competition_code), competition_type=VALUES(competition_type), competition_emblem=VALUES(competition_emblem)
        """, (competition['id'], competition_name, competition['code'], competition['type'], competition['emblem']))


        # Insert Match
        match_utc_date = datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
        match_utc_date = match_utc_date.strftime('%Y-%m-%d %H:%M:%S')
        
        last_updated = datetime.strptime(match['lastUpdated'], '%Y-%m-%dT%H:%M:%SZ')
        last_updated = last_updated.strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            INSERT INTO matches (match_id, match_utc_date, status, matchday, stage, last_updated, home_team_id, away_team_id, season_id, competition_id, area_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                match_utc_date = VALUES(match_utc_date),
                status = VALUES(status),
                matchday = VALUES(matchday),
                stage = VALUES(stage),
                last_updated = VALUES(last_updated),
                home_team_id = VALUES(home_team_id),
                away_team_id = VALUES(away_team_id),
                season_id = VALUES(season_id),
                competition_id = VALUES(competition_id),
                area_id = VALUES(area_id)
        """, (
            match['id'], match_utc_date, match['status'], match['matchday'], match['stage'], 
            last_updated, match['homeTeam']['id'], match['awayTeam']['id'], 
            match['season']['id'], match['competition']['id'], match['area']['id']
        ))

        # Insert Score
        cursor.execute("""
            INSERT INTO scores (match_id, winner, duration, full_time_home, full_time_away, half_time_home, half_time_away)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                winner = VALUES(winner),
                duration = VALUES(duration),
                full_time_home = VALUES(full_time_home),
                full_time_away = VALUES(full_time_away),
                half_time_home = VALUES(half_time_home),
                half_time_away = VALUES(half_time_away)
        """, (
            match['id'], match['score']['winner'], match['score']['duration'], 
            match['score']['fullTime']['home'], match['score']['fullTime']['away'], 
            match['score']['halfTime']['home'], match['score']['halfTime']['away']
        ))

        # Insert Referees
        for referee in match['referees']:
            cursor.execute("""
                INSERT INTO referees (referee_id, referee_name, referee_type, nationality)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE referee_name=VALUES(referee_name), referee_type=VALUES(referee_type), nationality=VALUES(nationality)
            """, (referee['id'], referee['name'], referee['type'], referee['nationality']))

            cursor.execute("""
                INSERT INTO match_referees (match_id, referee_id) 
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE match_id=match_id, referee_id=referee_id
            """, (match['id'], referee['id']))

# Commit and close connection
db.commit()
cursor.close()
db.close()

# Print total number of matches
print(f"Total matches found: {len(matches)}")