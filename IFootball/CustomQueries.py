import mysql.connector
import random
from QueryTexts import QueryTexts
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

        
DATABASE_URI = 'mysql+mysqlconnector://root:4444@localhost/IFootball'

Base = declarative_base()
engine = create_engine(DATABASE_URI)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="4444",
    database="IFootball"
)
cursor = db.cursor()

class CustomQueries:

    def get_custom_competitions():
        query = """
        SELECT 
            competition_id, 
            competition_name
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
                    "competition_name": row[1]
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
    
    def generate_custom_team_id():
        while True:
            team_id = random.randint(10000, 11000)
            cursor.execute("SELECT team_id FROM teams WHERE team_id = %s", (team_id,))
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
       
            query_competition = """
                DELETE FROM competitions
                WHERE competition_id = %s
            """
            cursor.execute(query_competition, (comp_id,))
            db.commit()
    
        except Exception as e:
            db.rollback()
            print(f"Failed to delete competition and teams: {str(e)}")

            
    def add_team_to_competition(team_info):
        team_id = CustomQueries.generate_custom_team_id()

        new_team = CustomTeams(
            team_id=team_id,
            competition_id=team_info['competition_id'],
            team_name=team_info['team_name'],
            crest=team_info['crest']
        )

        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            session.add(new_team)
            session.commit()
            print(f"New team '{team_info['team_name']}' added successfully with ID: {team_id}")
        except Exception as e:
            session.rollback()
            print(f"Failed to add team: {str(e)}")
        finally:
            session.close()
            
    def add_match_tocompetition():
        print("match added")
       
class CustomTeams(Base):
    __tablename__ = 'custom_teams'
    
    team_id = Column(String(255), primary_key=True, nullable=False, unique=True)
    competition_id = Column(String(255), nullable=False)
    team_name = Column(String(255), nullable=False)
    crest = Column(String(255), nullable=False)

