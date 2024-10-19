import mysql.connector
from datetime import datetime, timedelta
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="4444",
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
            m.matchday,
            m.home_team_id,
            m.away_team_id            
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
                "matchday": row[7],
                "home_team_id": row[8],
                "away_team_id": row[9]
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


    def get_next_matches(team_id, limit=10):
        query = """
        SELECT 
            m.match_id, 
            ht.short_name AS home_team, 
            at.short_name AS away_team, 
            m.match_utc_date, 
            c.competition_name,   
            m.matchday,
            m.home_team_id,
            m.away_team_id          
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
                "matchday": row[5],  # Matchday
                "home_team_id": row[6],
                "away_team_id": row[7]
            }
            for row in matches
        ]
    
    def get_team_stats(team_id):
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

    def get_competition_stats(competition_id):
    # Query to get team stats (goals scored, goals conceded, yellow and red cards)
        query = """
        SELECT 
        t.short_name,
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
        0 AS yellow_cards,  
        0 AS red_cards,
        0 AS total_shots,
        0 AS on_target,
        0 AS offsides,
        0 AS fouls
    FROM teams t
    JOIN matches m ON (m.home_team_id = t.team_id OR m.away_team_id = t.team_id)
    JOIN scores s ON m.match_id = s.match_id
    WHERE m.competition_id = %s
    GROUP BY t.short_name
    ORDER BY t.short_name ASC
        """

        cursor.execute(query, (competition_id,))
        stats = cursor.fetchall()

        result = []
        for team in stats:
            team_stat = {
                "team_name": team[0],
                "matches_played": team[1]+team[2]+team[3],
                "goals_scored": team[4],
                "goals_conceded": team[5],
                "yellow_cards": team[6],  # currently 0
                "red_cards": team[7],
                "total_shots": team[8],
                "on_target": team[9],
                "offsides": team[10],
                "fouls": team[11]
            }
            result.append(team_stat)

        return result

    def get_fixtures(competition_id=None, last=2, next=2):
        # Default competition IDs if none is provided
        default_competition_ids = [2001, 2021, 2015, 2014, 2002, 2019]
    
        # Use provided competition_id or default if None
        if competition_id is None:
            competition_ids = default_competition_ids
        else:
            competition_ids = [competition_id]

        # Create placeholders for the query
        placeholders = ', '.join(['%s'] * len(competition_ids))
    
        # Query to get fixtures from the past 'last' weeks, current week, and next 'next' weeks
        query = f"""
        SELECT 
            m.match_utc_date,
            m.matchday,
            t1.short_name AS home_team,
            t2.short_name AS away_team,
            s.full_time_home AS home_score,
            s.full_time_away AS away_score,
            m.competition_id,
            m.home_team_id,
            m.away_team_id,
            CASE 
                WHEN m.match_utc_date < NOW() THEN 'Last Match'
                ELSE 'Next Match'
            END AS match_status
        FROM matches m
        JOIN teams t1 ON m.home_team_id = t1.team_id
        JOIN teams t2 ON m.away_team_id = t2.team_id
        JOIN scores s ON m.match_id = s.match_id
        WHERE m.competition_id IN ({placeholders})
        AND m.match_utc_date BETWEEN DATE_SUB(CURDATE(), INTERVAL %s WEEK)  -- From 'last' weeks ago
                            AND DATE_ADD(CURDATE(), INTERVAL %s WEEK)  -- To 'next' weeks in future
        ORDER BY m.match_utc_date ASC
        """

        # Prepare parameters for the query
        parameters = competition_ids + [last, next]

        # Execute query with parameters
        cursor.execute(query, parameters)
        fixtures = cursor.fetchall()

        result = []
        for fixture in fixtures:
            if competition_id==None:
                competition_name = ""
                if fixture[6] == 2001:
                    competition_name = "UCL"
                elif fixture[6] == 2021:
                    competition_name = "EPL"
                elif fixture[6] == 2015:
                    competition_name = "Ligue 1"
                elif fixture[6] == 2014:
                    competition_name = "LaLiga"
                elif fixture[6] == 2002:
                    competition_name = "Bundesliga"
                elif fixture[6] == 2019:
                    competition_name = "Serie A"

                appended_matchday = f"{competition_name} R{fixture[1]}"
                
                fixture_data = {
                    "match_date": fixture[0],
                    "matchday": appended_matchday,
                    "home_team": fixture[2],
                    "away_team": fixture[3],
                    "home_score": fixture[4],
                    "away_score": fixture[5],
                    "home_team_id": fixture[7],
                    "away_team_id": fixture[8]
                }
            else:
                fixture_data = {
                    "match_date": fixture[0],
                    "matchday": f"R{fixture[1]}",
                    "home_team": fixture[2],
                    "away_team": fixture[3],
                    "home_score": fixture[4],
                    "away_score": fixture[5],
                    "home_team_id": fixture[7],
                    "away_team_id": fixture[8]
                }
                
            # If no competition_id is provided, add the default competition IDs to the result
            if competition_id is None:
                fixture_data["default_competition_ids"] = default_competition_ids
        
            result.append(fixture_data)

        return result



    def get_league_matches(league_id):
        """
        Fetch all matches for a given league without a limit.
        """
        today = datetime.utcnow().date()
        past_date = today - timedelta(days=15)
        future_date = today + timedelta(days=17)

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
        JOIN competitions c ON m.competition_id = c.competition_id
        WHERE m.competition_id = %s
          AND m.match_utc_date BETWEEN %s AND %s
        ORDER BY m.match_utc_date ASC
    """
    # Execute the query with the parameters
        cursor.execute(query, (league_id, past_date, future_date))
        matches = cursor.fetchall()  
        result = []
        for match in matches:
            fixture_data = {
                "match_id": match[0],
                "home_team": match[1],
                "away_team": match[2],
                "home_score": match[3] if match[3] is not None else "N/A",
                "away_score": match[4] if match[4] is not None else "N/A",
                "date": match[5].strftime('%Y-%m-%d'),
                "competition": match[6],
                "matchday": match[7]
            
            }
            result.append(fixture_data)
        return result

    def get_main_matches():
        """
        Fetch all main matches without a limit.
        """
        today = datetime.utcnow().date()
        past_date = today - timedelta(days=13)
        future_date = today + timedelta(days=15)

        query = """
        SELECT 
            m.match_id,
            t1.short_name AS home_team,
            t2.short_name AS away_team,
            s.full_time_home,
            s.full_time_away,
            m.match_utc_date,
            c.competition_name,
            m.matchday,
            m.home_team_id,
            m.away_team_id
        FROM matches m
        JOIN teams t1 ON m.home_team_id = t1.team_id
        JOIN teams t2 ON m.away_team_id = t2.team_id
        LEFT JOIN scores s ON m.match_id = s.match_id
        JOIN competitions c ON m.competition_id = c.competition_id
          AND m.match_utc_date BETWEEN %s AND %s
        ORDER BY m.competition_name
        ORDER BY m.match_utc_date ASC
    """
    # Execute the query with the parameters
        cursor.execute(query, ( past_date, future_date))
        matches = cursor.fetchall()
        result = []
        for match in matches:
            fixture_data = {
                "match_id": match[0],
                "home_team": match[1],
                "away_team": match[2],
                "home_score": match[3] if match[3] is not None else "N/A",
                "away_score": match[4] if match[4] is not None else "N/A",
                "date": match[5].strftime('%Y-%m-%d'),
                "competition": match[6],
                "matchday": match[7],
                "home_team_id": match[8],
                "away_team_id": match[9]
            }
            result.append(fixture_data)
        return result

    # def get_subscribed_matches(user_id):
    #     """
    #     Fetch all matches that a user is subscribed to without a limit.
    #     """
    #     query = """
    #     SELECT 
    #         m.match_id,
    #         t1.short_name AS home_team,
    #         t2.short_name AS away_team,
    #         s.full_time_home,
    #         s.full_time_away,
    #         m.match_utc_date,
    #         c.competition_name,
    #         m.matchday
    #     FROM matches m
    #     JOIN teams t1 ON m.home_team_id = t1.team_id
    #     JOIN teams t2 ON m.away_team_id = t2.team_id
    #     LEFT JOIN scores s ON m.match_id = s.match_id
    #     JOIN competitions c ON m.competition_id = c.competition_id
    #     JOIN user_subscriptions us ON us.match_id = m.match_id
    #     WHERE us.user_id = %s
    #     ORDER BY m.match_utc_date ASC
    #     """
    #     cursor.execute(query, (user_id,))
    #     matches = cursor.fetchall()

    #     return [
    #         {
    #             "match_id": row[0],
    #             "home_team": row[1],
    #             "away_team": row[2],
    #             "home_score": row[3] if row[3] is not None else "N/A",
    #             "away_score": row[4] if row[4] is not None else "N/A",
    #             "date": row[5].strftime('%Y-%m-%d'),
    #             "competition": row[6],
    #             "matchday": row[7]
    #         }
    #         for row in matches
    #     ]




    def get_player_stats(competition_id):
        # Initialize result dictionary to hold player stats
        result = {
            "top_scorers": [],
            "top_assist_providers": [],
            "top_yellow_card_recipients": [],
            "top_red_card_recipients": [],
            "top_clean_sheet_providers": []
        }

        # Query for top scorers
        query_top_scorers = """
        SELECT 
            ps.player_name,
            SUM(ps.goals) AS total_goals
        FROM player_stats ps
        WHERE ps.competition_id = %s
        GROUP BY ps.player_name
        ORDER BY total_goals DESC
        LIMIT 5;
        """
        cursor.execute(query_top_scorers, (competition_id,))
        top_scorers = cursor.fetchall()

        for player in top_scorers:
            result["top_scorers"].append({
                "player_name": player[0],
                "total_goals": player[1]
            })

        # Query for top assist providers
        query_top_assists = """
        SELECT 
            ps.player_name,
            SUM(ps.assists) AS total_assists
        FROM player_stats ps
        WHERE ps.competition_id = %s
        GROUP BY ps.player_name
        ORDER BY total_assists DESC
        LIMIT 5;
        """
        cursor.execute(query_top_assists, (competition_id,))
        top_assist_providers = cursor.fetchall()

        for player in top_assist_providers:
            result["top_assist_providers"].append({
                "player_name": player[0],
                "total_assists": player[1]
            })

        # Query for top yellow card recipients
        query_top_yellow_cards = """
        SELECT 
            ps.player_name,
            SUM(ps.yellow_cards) AS total_yellow_cards
        FROM player_stats ps
        WHERE ps.competition_id = %s
        GROUP BY ps.player_name
        ORDER BY total_yellow_cards DESC
        LIMIT 5;
        """
        cursor.execute(query_top_yellow_cards, (competition_id,))
        top_yellow_card_recipients = cursor.fetchall()

        for player in top_yellow_card_recipients:
            result["top_yellow_card_recipients"].append({
                "player_name": player[0],
                "total_yellow_cards": player[1]
            })

        # Query for top red card recipients
        query_top_red_cards = """
        SELECT 
            ps.player_name,
            SUM(ps.red_cards) AS total_red_cards
        FROM player_stats ps
        WHERE ps.competition_id = %s
        GROUP BY ps.player_name
        ORDER BY total_red_cards DESC
        LIMIT 5;
        """
        cursor.execute(query_top_red_cards, (competition_id,))
        top_red_card_recipients = cursor.fetchall()

        for player in top_red_card_recipients:
            result["top_red_card_recipients"].append({
                "player_name": player[0],
                "total_red_cards": player[1]
            })

        # Query for top clean sheet providers
        query_top_clean_sheets = """
        SELECT 
            ps.player_name,
            SUM(ps.clean_sheets) AS total_clean_sheets
        FROM player_stats ps
        WHERE ps.competition_id = %s
        GROUP BY ps.player_name
        ORDER BY total_clean_sheets DESC
        LIMIT 5;
        """
        cursor.execute(query_top_clean_sheets, (competition_id,))
        top_clean_sheet_providers = cursor.fetchall()

        for player in top_clean_sheet_providers:
            result["top_clean_sheet_providers"].append({
                "player_name": player[0],
                "total_clean_sheets": player[1]
            })

        return result