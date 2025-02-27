
import mysql.connector
import requests
from datetime import datetime, timedelta

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="210041139",
    database="IFootball"
)
cursor = db.cursor()
new_user = False
cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
cursor.execute("SELECT COUNT(*) FROM matches")
match_count = cursor.fetchone()[0]

if match_count > 0: 
    cursor.execute("SELECT MAX(match_utc_date) FROM matches WHERE status = 'FINISHED'")
    result = cursor.fetchone()
    earliest_date = result[0]
    start_date =earliest_date.strftime('%Y-%m-%d')  
    end_date = (datetime.now() + timedelta(1)).strftime('%Y-%m-%d')
    
else:
    start_date = '2024-08-01'  
    end_date = (datetime.now() + timedelta(1)).strftime('%Y-%m-%d')
    new_user = True
    
API_TOKEN = '8511ddac058c4982b7c64722e71b77ee'
headers = {'X-Auth-Token': API_TOKEN}

def fetch_matches_for_date_range(start, end):
    print(f"Fetching matches from {start} to {end}")
    uri = f'https://api.football-data.org/v4/matches?dateFrom={start}&dateTo={end}'
    response = requests.get(uri, headers=headers)
    
    if response.status_code == 200:
        return response.json()['matches']
    else:
        print(f"Failed to fetch data from {start} to {end}. Status code: {response.status_code}")
        return []

# Break the date range into 7-day intervals and fetch data
def fetch_matches_in_intervals(start_date, end_date):
    current_start = datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=1)
    final_end = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
    all_matches = []

    while current_start <= final_end:
        current_end = current_start + timedelta(days=7)
        if current_end > final_end:
            current_end = final_end
        print(f"Fetching from {current_start.strftime('%Y-%m-%d')} to {current_end.strftime('%Y-%m-%d')}")

        matches = fetch_matches_for_date_range(current_start.strftime('%Y-%m-%d'), current_end.strftime('%Y-%m-%d'))
        all_matches.extend(matches)

        current_start = current_end + timedelta(days=1)
    
    return all_matches

matches = fetch_matches_in_intervals(start_date, end_date)

for match in matches:
    competition_id = match['competition']['id']
    
    if competition_id >0: 
        if new_user:
            area = match['area']
            cursor.execute("""
                INSERT INTO areas (area_id, area_name, area_code, area_flag)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE area_name=VALUES(area_name), area_code=VALUES(area_code), area_flag=VALUES(area_flag)
            """, (area['id'], area['name'], area['code'], area['flag']))

            home_team = match['homeTeam']
            if home_team['id'] is None:
                print(f"Warning: Home team has null team_id - {match}")
            else:
                cursor.execute("""
                    INSERT INTO teams (team_id, team_name, short_name, tla, crest)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE team_name=VALUES(team_name), short_name=VALUES(short_name), tla=VALUES(tla), crest=VALUES(crest)
                """, (home_team['id'], home_team['name'], home_team['shortName'], home_team['tla'], home_team['crest']))

            away_team = match['awayTeam']
            if away_team['id'] is None:
                print(f"Warning: Away team has null team_id - {away_team}")
            else:
                cursor.execute("""
                    INSERT INTO teams (team_id, team_name, short_name, tla, crest)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE team_name=VALUES(team_name), short_name=VALUES(short_name), tla=VALUES(tla), crest=VALUES(crest)
                """, (away_team['id'], away_team['name'], away_team['shortName'], away_team['tla'], away_team['crest']))

            season = match['season']
            cursor.execute("""
                INSERT INTO seasons (season_id, start_date, end_date, current_matchday)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE start_date=VALUES(start_date), end_date=VALUES(end_date), current_matchday=VALUES(current_matchday)
            """, (season['id'], season['startDate'], season['endDate'], season['currentMatchday']))

            competition = match['competition']
            competition_name = competition['name']
            if competition_name.lower() == 'primera division':
                competition_name = 'LaLiga'

            cursor.execute("""
                INSERT INTO competitions (competition_id, competition_name, competition_code, competition_type, competition_emblem)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE competition_name=VALUES(competition_name), competition_code=VALUES(competition_code), competition_type=VALUES(competition_type), competition_emblem=VALUES(competition_emblem)
            """, (competition['id'], competition_name, competition['code'], competition['type'], competition['emblem']))

        # Check if teams exist before inserting into matches
        cursor.execute("SELECT COUNT(*) FROM teams WHERE team_id = %s", (match['homeTeam']['id'],))
        home_team_exists = cursor.fetchone()[0] > 0
        
        if not home_team_exists:
            home_team = match['homeTeam']
            cursor.execute("""
                    INSERT INTO teams (team_id, team_name, short_name, tla, crest)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE team_name=VALUES(team_name), short_name=VALUES(short_name), tla=VALUES(tla), crest=VALUES(crest)
                """, (home_team['id'], home_team['name'], home_team['shortName'], home_team['tla'], home_team['crest']))

        cursor.execute("SELECT COUNT(*) FROM teams WHERE team_id = %s", (match['awayTeam']['id'],))
        away_team_exists = cursor.fetchone()[0] > 0

        if not away_team_exists:
            away_team = match['homeTeam']
            cursor.execute("""
                    INSERT INTO teams (team_id, team_name, short_name, tla, crest)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE team_name=VALUES(team_name), short_name=VALUES(short_name), tla=VALUES(tla), crest=VALUES(crest)
                """, (away_team['id'], away_team['name'], away_team['shortName'], away_team['tla'], away_team['crest']))

        
        match_utc_date = datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
        match_utc_date = match_utc_date.strftime('%Y-%m-%d %H:%M:%S')

        last_updated = datetime.strptime(match['lastUpdated'], '%Y-%m-%dT%H:%M:%SZ')
        last_updated = last_updated.strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
            INSERT INTO matches (match_id, match_utc_date, status, matchday, stage, last_updated, home_team_id, away_team_id, season_id, competition_id, area_id)
            VALUES (%s, DATE_ADD(%s, INTERVAL 6 HOUR), %s, %s, %s, %s, %s, %s, %s, %s, %s)
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


db.commit()
cursor.close()
db.close()

print(f"Total matches found: {len(matches)}")