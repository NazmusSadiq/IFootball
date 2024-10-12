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
            cursor.execute("SELECT short_name FROM teams")

            # Fetch all team names and return them as a list
            teams = [row[0] for row in cursor.fetchall()]
            return teams
        except Exception as e:
            print(f"Error fetching teams from database: {e}")
            return []
        
    ## Query to get Team_Id based on Team_Name   
    def get_team_id_by_name(short_name):
        query = "SELECT team_id FROM teams WHERE short_name = %s"
        cursor.execute(query, (short_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    # queries.py

    def get_last_matches(team_id, limit=10):
        query = """
        SELECT 
            m.match_id, 
            t1.short_name AS home_team, 
            t2.short_name AS away_team, 
            s.full_time_home, 
            s.full_time_away, 
            m.match_utc_date, 
            c.competition_name,  
            m.matchday            
        FROM matches m
        JOIN teams t1 ON m.home_team_id = t1.team_id
        JOIN teams t2 ON m.away_team_id = t2.team_id
        LEFT JOIN scores s ON m.match_id = s.match_id
        JOIN competitions c ON m.competition_id = c.competition_id -- Join to get competition name
        WHERE (m.home_team_id = %s OR m.away_team_id = %s) 
          AND m.match_utc_date <= NOW()
        ORDER BY m.match_utc_date ASC
        LIMIT %s
        """
        cursor.execute(query, (team_id, team_id, limit))
        matches = cursor.fetchall()

        return [
            {
                "match_id": row[0],
                "team1": row[1],
                "team2": row[2],
                "score1": row[3] if row[3] is not None else "N/A",  
                "score2": row[4] if row[4] is not None else "N/A",  
                "date": row[5].strftime('%Y-%m-%d'),  
                "competition": row[6],  
                "matchday": row[7]  
            }
            for row in matches
        ]




    def get_next_matches(team_id, limit=10):
        query = """
        SELECT 
            m.match_id, 
            ht.short_name AS home_team, 
            at.short_name AS away_team, 
            m.match_utc_date, 
            c.competition_name,   
            m.matchday           
        FROM matches m
        JOIN teams ht ON m.home_team_id = ht.team_id
        JOIN teams at ON m.away_team_id = at.team_id
        JOIN competitions c ON m.competition_id = c.competition_id  -- Join to get competition name
        WHERE (m.home_team_id = %s OR m.away_team_id = %s) 
          AND m.match_utc_date > NOW()
        ORDER BY m.match_utc_date ASC
        LIMIT %s
        """
        cursor.execute(query, (team_id, team_id, limit))
        matches = cursor.fetchall()

        # Returning the match details
        return [
            {
                "match_id": row[0],
                "team1": row[1],  # home team
                "team2": row[2],  # away team
                "date": row[3].strftime('%Y-%m-%d'),  # match date in 'YYYY-MM-DD' format
                "competition": row[4],  # Competition name
                "matchday": row[5]  # Matchday
            }
            for row in matches
        ]
    
    def get_team_stats_in_fav(team_id):
        # Query to get overall team stats by competition
        query = """
        SELECT 
            c.competition_name, 
            COUNT(m.match_id) AS total_matches,
            SUM(CASE 
                WHEN (m.home_team_id = %s AND s.full_time_home > s.full_time_away) OR (m.away_team_id = %s AND s.full_time_away > s.full_time_home) THEN 1 
                ELSE 0 
            END) AS wins,
            SUM(CASE 
                WHEN s.full_time_home = s.full_time_away THEN 1 
                ELSE 0 
            END) AS draws,
            SUM(CASE 
                WHEN (m.home_team_id = %s AND s.full_time_home < s.full_time_away) OR (m.away_team_id = %s AND s.full_time_away < s.full_time_home) THEN 1 
                ELSE 0 
            END) AS losses,
            SUM(CASE 
                WHEN m.home_team_id = %s THEN s.full_time_home 
                ELSE s.full_time_away 
            END) AS goals_scored,
            SUM(CASE 
                WHEN m.home_team_id = %s THEN s.full_time_away 
                ELSE s.full_time_home 
            END) AS goals_conceded
        FROM matches m
        JOIN scores s ON m.match_id = s.match_id
        JOIN competitions c ON m.competition_id = c.competition_id
        WHERE m.home_team_id = %s OR m.away_team_id = %s
        GROUP BY c.competition_name
        """
        cursor.execute(query, (team_id, team_id, team_id, team_id, team_id, team_id, team_id, team_id))
        stats = cursor.fetchall()

        # Query to get the biggest win by competition
        biggest_win_query = """
        SELECT 
            c.competition_name,
            m.match_utc_date,
            t2.short_name AS opponent,
            GREATEST(ABS(s.full_time_home - s.full_time_away), 0) AS goal_difference,
            CASE 
                WHEN m.home_team_id = %s THEN s.full_time_home 
                ELSE s.full_time_away 
            END AS team_goals,
            CASE 
                WHEN m.home_team_id = %s THEN s.full_time_away 
                ELSE s.full_time_home 
            END AS opponent_goals,
            m.matchday 
        FROM matches m
        JOIN teams t2 ON (m.home_team_id = t2.team_id OR m.away_team_id = t2.team_id) AND t2.team_id != %s
        JOIN scores s ON m.match_id = s.match_id
        JOIN competitions c ON m.competition_id = c.competition_id
        WHERE (m.home_team_id = %s OR m.away_team_id = %s) 
          AND ((m.home_team_id = %s AND s.full_time_home > s.full_time_away) OR (m.away_team_id = %s AND s.full_time_away > s.full_time_home))
        ORDER BY c.competition_name, goal_difference DESC, m.match_utc_date DESC
        """
        # Execute the query to fetch biggest wins
        cursor.execute(biggest_win_query, (team_id, team_id, team_id, team_id, team_id, team_id, team_id))
        biggest_wins = cursor.fetchall()

        # Dictionary to hold the biggest win for each competition
        biggest_win_dict = {}

        for win in biggest_wins:
            competition_name = win[0]
            goal_difference = win[3]

            # Check if this competition already has a biggest win
            if competition_name in biggest_win_dict:
                # If current goal_difference is greater, replace the existing biggest win
                if goal_difference > biggest_win_dict[competition_name]['goal_difference']:
                    biggest_win_dict[competition_name] = {
                        "date": win[1].strftime('%Y-%m-%d'),
                        "opponent": win[2],
                        "goal_difference": goal_difference,
                        "team_goals": win[4],
                        "opponent_goals": win[5],
                        "matchday": win[6]  # Add match day
                    }
            else:
                # If no entry for this competition, add it
                biggest_win_dict[competition_name] = {
                    "date": win[1].strftime('%Y-%m-%d'),
                    "opponent": win[2],
                    "goal_difference": goal_difference,
                    "team_goals": win[4],
                    "opponent_goals": win[5],
                    "matchday": win[6]  # Add match day
                }

        # Formatting the result
        result = []
        for stat in stats:
            biggest_win = biggest_win_dict.get(stat[0])  # Get the biggest win for the competition, or None if not available

            competition_stat = {
                "competition": stat[0],
                "total_matches": stat[1],
                "wins": stat[2],
                "draws": stat[3],
                "losses": stat[4],
                "goals_scored": stat[5],
                "goals_conceded": stat[6],
                "goal_difference": stat[5] - stat[6],
                "biggest_win": biggest_win  # Pass the single biggest win for each competition if available
            }

            result.append(competition_stat)

        return result

    def get_competition_standings(competition_id):
    # Query to get team standings for the given competition
        query = """
        SELECT 
            t.short_name,
            SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home > s.full_time_away) OR (m.away_team_id = t.team_id AND s.full_time_away > s.full_time_home) THEN 3 
                WHEN s.full_time_home = s.full_time_away THEN 1 
                ELSE 0 
            END) AS points,
            SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home > s.full_time_away) OR (m.away_team_id = t.team_id AND s.full_time_away > s.full_time_home) THEN 1 
                ELSE 0 
            END) AS wins,
            SUM(CASE WHEN s.full_time_home = s.full_time_away THEN 1 ELSE 0 END) AS draws,
            SUM(CASE 
                WHEN (m.home_team_id = t.team_id AND s.full_time_home < s.full_time_away) OR (m.away_team_id = t.team_id AND s.full_time_away < s.full_time_home) THEN 1 
                ELSE 0 
            END) AS losses,
            SUM(CASE 
                WHEN m.home_team_id = t.team_id THEN s.full_time_home 
                ELSE s.full_time_away 
            END) AS goals_scored,
            SUM(CASE 
                WHEN m.home_team_id = t.team_id THEN s.full_time_away 
                ELSE s.full_time_home 
            END) AS goals_conceded,
            (SUM(CASE 
                WHEN m.home_team_id = t.team_id THEN s.full_time_home 
                ELSE s.full_time_away 
            END) - SUM(CASE 
                WHEN m.home_team_id = t.team_id THEN s.full_time_away 
                ELSE s.full_time_home 
            END)) AS goal_difference
        FROM teams t
        JOIN matches m ON (m.home_team_id = t.team_id OR m.away_team_id = t.team_id)
        JOIN scores s ON m.match_id = s.match_id
        WHERE m.competition_id = %s
        GROUP BY t.short_name
        ORDER BY points DESC, goal_difference DESC, goals_scored DESC
        """

        cursor.execute(query, (competition_id,))
        standings = cursor.fetchall()

        result = []
        for team in standings:
            team_stat = {
                "team_name": team[0],
                "points": team[1],
                "wins": team[2],
                "draws": team[3],
                "losses": team[4],
                "goals_scored": team[5],
                "goals_conceded": team[6],
                "goal_difference": team[7]
            }
            result.append(team_stat)

        return result



