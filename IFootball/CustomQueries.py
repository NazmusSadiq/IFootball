import os
import mysql.connector
import random
from QueryTexts import QueryTexts
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="4444",
    database="IFootball"
)
cursor = db.cursor()
DATABASE_URI = 'mysql+mysqlconnector://root:4444@localhost/IFootball'
Base = declarative_base()
engine = create_engine(DATABASE_URI) 

class CustomTeams(Base):
    __tablename__ = 'custom_teams'
    
    team_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    competition_id = Column(Integer, nullable=False)
    team_name = Column(String(255), nullable=False)
    crest = Column(String(255), nullable=False)

class CustomMatches(Base):
    __tablename__ = 'custom_matches'
    
    match_id = Column(Integer, primary_key=True, nullable=False, unique=True)
    status = Column(String(45), nullable=False)
    home_team_id = Column(Integer, nullable=False)
    away_team_id = Column(Integer, nullable=False)
    competition_id = Column(String(255), nullable=False)
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    serial = Column(Integer, nullable = False)
    round = Column(Integer ,nullable = False)

class CustomQueries:  

    def get_custom_competitions():
        query = """
        SELECT 
            competition_id, 
            competition_name,
            competition_emblem
        FROM competitions
        WHERE competition_id < 10
        ORDER BY competition_id ASC
        """
        try:
            cursor.execute(query)
            competitions = cursor.fetchall()
            return [
                {
                    "competition_id": row[0],
                    "competition_name": row[1],
                    "competition_emblem": row[2]
                }
                for row in competitions
            ]
        except Exception as e:
            print(f"Error executing query: {e}")
            return []

    def generate_custom_competition_id():
        while True:
            competition_id = random.randint(1, 9)
            cursor.execute("SELECT competition_id FROM competitions WHERE competition_id = %s", (competition_id,))
            if cursor.fetchone() is None:
                break
        return competition_id
    
    def generate_custom_match_id():
        cursor.execute("LOCK TABLES custom_matches WRITE")
        try:
            while True:
                match_id = random.randint(1, 10000)
                cursor.execute("SELECT match_id FROM custom_matches WHERE match_id = %s", (match_id,))
                if cursor.fetchone() is None:
                    break
        finally:
            cursor.execute("UNLOCK TABLES")
        return match_id

    
    def generate_custom_team_id():
        while True:
            team_id = random.randint(10000, 11000)
            cursor.execute("SELECT team_id FROM custom_teams WHERE team_id = %s", (team_id,))
            if cursor.fetchone() is None:
                break
        return team_id
    
    def add_to_existing_competitions(competition):
        query = QueryTexts.add_to_existing_competition_query
        cursor = db.cursor()
        cursor.execute(query, (
            competition['id'],
            competition['name'],
            competition['code'],
            competition['type'],
            competition['emblem']
        ))
        db.commit()

    def delete_competition(comp_id):
        try:
            query_teams = """
                DELETE FROM custom_teams
                WHERE competition_id = %s
            """
            cursor.execute(query_teams, (comp_id,))
        
            query_matches = """
                DELETE FROM custom_matches
                WHERE competition_id = %s
            """
            cursor.execute(query_matches, (comp_id,))
        
            query_competition = """
                DELETE FROM competitions
                WHERE competition_id = %s
            """
            cursor.execute(query_competition, (comp_id,))
        
            db.commit()
            print(f"Competition {comp_id} and its associated teams, matches, and competition details were deleted successfully.")
    
        except Exception as e:
            db.rollback()
            print(f"Failed to delete competition and associated data: {str(e)}")
           
    def add_team_to_competition(team_info):
        team_id = CustomQueries.generate_custom_team_id()
        
        insert_team_query = """
            INSERT INTO custom_teams (team_id, competition_id, team_name, crest)
            VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(insert_team_query, (
                team_id,
                team_info['competition_id'],
                team_info['team_name'],
                team_info['crest']
            ))
            db.commit()
            print(f"New team '{team_info['team_name']}' added successfully with ID: {team_id}")
        except Exception as e:
            db.rollback()
            print(f"Failed to add team: {str(e)}")
            
    def get_team_stats_of_competition(comp_id):
        print()
        
    def get_competition_standings(competition_id):
        query = QueryTexts.custom_competition_standings_query
        cursor.execute(query, (competition_id, competition_id))
        standings = cursor.fetchall()
        print(f"id:{competition_id}")
        result = []
        for index, team in enumerate(standings):
            team_stat = {
                "team_name": team[0],
                "points": team[1],
                "wins": team[2],
                "draws": team[3],
                "losses": team[4],
                "goals_scored": team[5],
                "goals_conceded": team[6],
                "goal_difference": team[7],
                "team_pos": index + 1
            }
            result.append(team_stat)
        return result
     
    def create_new_fixture(comp_id):
        try:
            # Fetch all teams in the competition
            fetch_teams_query = """
                SELECT team_id FROM custom_teams WHERE competition_id = %s
            """
            cursor.execute(fetch_teams_query, (comp_id,))
            teams = [row[0] for row in cursor.fetchall()]
            num_teams = len(teams)
        
            if num_teams < 2:
                print("Not enough teams for a competition.")
                return

            # Ensure even number of teams by adding a dummy team if needed
            if num_teams % 2 != 0:
                teams.append("BYE")  # Add a "bye" team for odd team count
                num_teams += 1

            print(f"Total teams: {num_teams} (including BYE if needed)")

            # List to store match data
            matches = []
            current_serial = 1

            # Generate the rounds
            rounds = []
            for round_num in range(num_teams - 1):
                round_matches = []
                for i in range(num_teams // 2):
                    home_team = teams[i]
                    away_team = teams[num_teams - 1 - i]
                    if home_team != "BYE" and away_team != "BYE":
                        round_matches.append({
                            "home_team_id": home_team,
                            "away_team_id": away_team,
                            "round": round_num + 1
                        })
                rounds.append(round_matches)
                # Rotate teams clockwise, leaving the first team fixed
                teams = [teams[0]] + [teams[-1]] + teams[1:-1]

            for round_num, round_matches in enumerate(rounds, start=1):  
                for match in round_matches:
                    matches.append({
                        "match_id": CustomQueries.generate_custom_match_id(),
                        "status": "Unfinished",
                        "home_team_id": match["home_team_id"],
                        "away_team_id": match["away_team_id"],
                        "competition_id": comp_id,
                        "home_score": None,
                        "away_score": None,
                        "serial": current_serial,
                        "round": round_num
                    })
                    current_serial += 1

            for round_num, round_matches in enumerate(rounds, start=len(rounds) +1):  
                for match in round_matches:
                    matches.append({
                        "match_id": CustomQueries.generate_custom_match_id(),
                        "status": "Unfinished",
                        "home_team_id": match["away_team_id"],  
                        "away_team_id": match["home_team_id"],
                        "competition_id": comp_id,
                        "home_score": None,
                        "away_score": None,
                        "serial": current_serial,
                        "round": round_num
                    })
                    current_serial += 1


            # Insert matches into the database
            insert_match_query = """
                INSERT INTO custom_matches (match_id, status, home_team_id, away_team_id, competition_id, home_score, away_score, serial, round)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            for match in matches:
                cursor.execute(insert_match_query, (
                    match["match_id"],
                    match["status"],
                    match["home_team_id"],
                    match["away_team_id"],
                    match["competition_id"],
                    match["home_score"],
                    match["away_score"],
                    match["serial"],
                    match["round"]
                ))

            db.commit()
            print(f"Fixture created successfully for competition ID: {comp_id}")

        except Exception as e:
            db.rollback()
            print(f"Failed to create fixture: {str(e)}")


    def get_team_crest(team_id):
        query = "SELECT crest FROM custom_teams WHERE team_id = %s"
        cursor.execute(query, (team_id,))
        crest_path = cursor.fetchone()
        crest_path = crest_path[0]
        from PyQt5 import QtWidgets as qtw
        from PyQt5 import QtCore as qtc, QtGui as qtg
        
        if os.path.exists(crest_path):
            pixmap = qtg.QPixmap(crest_path).scaled(20, 20, qtc.Qt.KeepAspectRatio)
        else:
            pixmap = qtg.QPixmap(20, 20)
            pixmap.fill(qtg.QColor("gray"))
        label = qtw.QLabel()
        label.setPixmap(pixmap)
        return label
    def get_team_name(team_id):
        query = "SELECT team_name FROM custom_teams WHERE team_id = %s"
        cursor.execute(query, (team_id,))
        team_name = cursor.fetchone()[0]
        return team_name
    def get_fixtures(comp_id, last=20, next=20):
        try:
            query = f"""
            SELECT * FROM custom_matches
            WHERE competition_id = %s
            ORDER BY serial ASC
            """
   
            cursor.execute(query, (comp_id,))
            matches = cursor.fetchall()
            last_played_serial_query = f"""
            SELECT MAX(serial)
            FROM custom_matches
            WHERE competition_id = %s AND status != 'Unfinished'
            """
            cursor.execute(last_played_serial_query, (comp_id,))
            last_played_serial = cursor.fetchone()[0]

            if not last_played_serial:
                upcoming_matches = [match for match in matches if match[1] == 'Unfinished']
                next_matches = upcoming_matches[:next] if upcoming_matches else []

                result = []
                for match in next_matches:
                    
                    home_team_name = CustomQueries.get_team_name(match[2])
                    
                    away_team_name = CustomQueries.get_team_name(match[3])
                
                    result.append({
                        "match_id": match[0],
                        "status": match[1],
                        "home_team_id": match[2],
                        "home_team": home_team_name,
                        "away_team_id": match[3],
                        "away_team": away_team_name,
                        "competition_id": match[4],
                        "home_score": match[5],
                        "away_score": match[6],
                        "serial": match[7],
                        "matchday": match[8]
                    })
                return result
            played_matches = [match for match in matches if match[7] <= last_played_serial]
            upcoming_matches = [match for match in matches if match[7] > last_played_serial]

            last_matches = played_matches[-last:] if played_matches else []
            next_matches = upcoming_matches[:next] if upcoming_matches else []

            filtered_matches = last_matches + next_matches

            result = []
            for match in filtered_matches:
                cursor.execute(
                    "SELECT team_name FROM custom_teams WHERE team_id = %s",
                    (match[2],)
                )
                home_team_name = cursor.fetchone()[0]
                cursor.execute(
                    "SELECT team_name FROM custom_teams WHERE team_id = %s",
                    (match[3],)
                )
                away_team_name = cursor.fetchone()[0]

                result.append({
                    "match_id": match[0],
                    "status": match[1],
                    "home_team_id": match[2],
                    "home_team": home_team_name,
                    "away_team_id": match[3],
                    "away_team": away_team_name,
                    "competition_id": match[4],
                    "home_score": match[5],
                    "away_score": match[6],
                    "serial": match[7],
                    "matchday": match[8]
                })

            return result

        except Exception as e:
            print(f"Error fetching fixtures: {e}")
            return []

            played_matches = [match for match in matches if match[7] <= last_played_serial]
            upcoming_matches = [match for match in matches if match[7] > last_played_serial]

            last_matches = played_matches[-last:] if played_matches else []
            next_matches = upcoming_matches[:next] if upcoming_matches else []

            filtered_matches = last_matches + next_matches

            result = [
                {
                    "match_id": match[0],
                    "status": match[1],
                    "home_team_id": match[2],
                    "away_team_id": match[3],
                    "competition_id": match[4],
                    "home_score": match[5],
                    "away_score": match[6]
                }
                for match in filtered_matches
            ]

            return result

        except Exception as e:
            print(f"Error fetching fixtures: {e}")
            return [] 
        
    def update_match(match_id, home_score, away_score):
        try:
            query = """
            UPDATE custom_matches
            SET home_score = %s, away_score = %s, status = %s
            WHERE match_id = %s
            """
            status = "Finished" if home_score is not None and away_score is not None else "Unfinished"

            cursor.execute(query, (home_score, away_score, status, match_id))
            db.commit()
            print(f"Match {match_id} updated successfully: {home_score}-{away_score}")
            return True
        except Exception as e:
            print(f"Error updating match {match_id}: {e}")
            db.rollback()
            return False
Base.metadata.create_all(engine)