import mysql.connector
from QueryTexts import QueryTexts
from datetime import datetime, timedelta

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="4444",
    database="IFootball"
)
cursor = db.cursor()

class Queries:
    
    fav_team_id=0
        
    def fetch_teams_from_database():
        try:
            cursor.execute("SELECT team_name FROM teams")

            teams = [row[0] for row in cursor.fetchall()]
            return teams
        except Exception as e:
            print(f"Error fetching teams from database: {e}")
            return []
         
    def get_team_id_by_name(full_name):
        query = "SELECT team_id FROM teams WHERE team_name = %s"
        cursor.execute(query, (full_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    
    def get_team_full_name_by_id(team_id):
        query = "SELECT team_name FROM teams WHERE team_id = %s"
        cursor.execute(query, (team_id,))
        result = cursor.fetchone()
        return result[0] if result else None

    def get_last_matches(team_id, limit=10):
        query = QueryTexts.last_matches_query
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
                "away_team_id": row[9],
                "subscribed": row[10]
            }
            for row in matches
        ]

    def get_team_stats_in_fav(team_id):
        query = QueryTexts.team_stats_in_fav
        cursor.execute(query, (team_id, team_id, team_id, team_id, team_id, team_id, team_id, team_id))
        stats = cursor.fetchall()

        biggest_win_query = QueryTexts.biggest_win_query
        cursor.execute(biggest_win_query, (team_id, team_id, team_id, team_id, team_id, team_id, team_id))
        biggest_wins = cursor.fetchall()

        biggest_loss_query = QueryTexts.biggest_loss_query
        cursor.execute(biggest_loss_query, (team_id, team_id, team_id, team_id, team_id, team_id, team_id))
        biggest_losses = cursor.fetchall()

        biggest_stats_dict = {}

        for win in biggest_wins:
            competition_name = win[0]
            goal_difference = win[3]
            if competition_name not in biggest_stats_dict:
                biggest_stats_dict[competition_name] = {'biggest_win': None, 'biggest_loss': None}
        
            if biggest_stats_dict[competition_name]['biggest_win'] is None or goal_difference > biggest_stats_dict[competition_name]['biggest_win']['goal_difference']:
                biggest_stats_dict[competition_name]['biggest_win'] = {
                    "date": win[1].strftime('%Y-%m-%d'),
                    "opponent": win[2],
                    "goal_difference": goal_difference,
                    "team_goals": win[4],
                    "opponent_goals": win[5],
                    "matchday": win[6]  
                }

        for loss in biggest_losses:
            competition_name = loss[0]
            goal_difference = loss[3]
            if competition_name not in biggest_stats_dict:
                biggest_stats_dict[competition_name] = {'biggest_win': None, 'biggest_loss': None}
        
            if biggest_stats_dict[competition_name]['biggest_loss'] is None or goal_difference > biggest_stats_dict[competition_name]['biggest_loss']['goal_difference']:
                biggest_stats_dict[competition_name]['biggest_loss'] = {
                    "date": loss[1].strftime('%Y-%m-%d'),
                    "opponent": loss[2],
                    "goal_difference": goal_difference,
                    "team_goals": loss[4],
                    "opponent_goals": loss[5],
                    "matchday": loss[6]  
                }

        result = []
        for stat in stats:
            competition_name = stat[0]
            biggest_stats = biggest_stats_dict.get(competition_name, {'biggest_win': None, 'biggest_loss': None})

            competition_stat = {
                "competition": stat[0],
                "competition_id": stat[1],
                "total_matches": stat[2],
                "wins": stat[3],
                "draws": stat[4],
                "losses": stat[5],
                "goals_scored": stat[6],
                "goals_conceded": stat[7],
                "goal_difference": stat[6] - stat[7],
                "biggest_win": biggest_stats['biggest_win'],
                "biggest_loss": biggest_stats['biggest_loss']
            }

            result.append(competition_stat)

        return result

    def get_next_matches(team_id, limit=10):
        query = QueryTexts.next_matches_query
        cursor.execute(query, (team_id, team_id, limit))
        matches = cursor.fetchall()

        return [
            {
                "match_id": row[0],
                "team1": row[1],  # home team
                "team2": row[2],  # away team
                "date": row[3].strftime('%Y-%m-%d'),  
                "competition": row[4],  
                "matchday": row[5],  
                "home_team_id": row[6],
                "away_team_id": row[7],
                "subscribed": row[8]
            }
            for row in matches
        ]

    def get_competition_standings(competition_id):
        query = QueryTexts.competition_standings_query
        cursor.execute(query, (competition_id,))
        standings = cursor.fetchall()

        result = []
        for team in standings:
            team_stat = {
                "team_name": team[0],
                "team_id": team[1],
                "points": team[2],
                "wins": team[3],
                "draws": team[4],
                "losses": team[5],
                "goals_scored": team[6],
                "goals_conceded": team[7],
                "goal_difference": team[8]
            }
            result.append(team_stat)

        return result

    def get_competition_standings_near_team(competition_id, team_id):
        
        query = QueryTexts.competition_standings_near_team_query
        cursor.execute(query, (competition_id,))
        standings = cursor.fetchall()

        team_position = next((index for index, team in enumerate(standings) if team[0] == team_id), None)
        if team_position is None:
            return []  
        
        start = max(0, team_position - 2)  
        end = min(len(standings), team_position + 3)  

        selected_standings = standings[start:end]

        result = []
        for index, team in enumerate(selected_standings, start=start):
            team_stat = {
                "team_id": team[0],
                "team_name": team[1],
                "points": team[2],
                "wins": team[3],
                "draws": team[4],
                "losses": team[5],
                "goals_scored": team[6],
                "goals_conceded": team[7],
                "goal_difference": team[8],
                "team_pos": index + 1  
            }
            result.append(team_stat)

        return result

    def get_competition_stats(competition_id):
        query = QueryTexts.competition_stats_query
        cursor.execute(query, (competition_id,))
        stats = cursor.fetchall()

        result = []
        for team in stats:
            team_stat = {
                "team_name": team[0],
                "matches_played": team[1]+team[2]+team[3],
                "goals_scored": team[4],
                "goals_conceded": team[5],
                "yellow_cards": team[6], 
                "red_cards": team[7],   
                "total_shots": team[8], 
                "on_target": team[9],   
                "offsides": team[10],   
                "fouls": team[11]   
            }
            result.append(team_stat)

        return result

    def get_fixtures(competition_id=None, last=2, next=2):
        default_competition_ids = [2001, 2021, 2015, 2014, 2002, 2019]
        if competition_id is None:
            competition_ids = default_competition_ids
        else:
            competition_ids = [competition_id]

        placeholders = ', '.join(['%s'] * len(competition_ids))
    
        query = QueryTexts.get_fixtures_query(placeholders)

        parameters = competition_ids + [last, next]

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
                    "away_team_id": fixture[8],
                    "match_id": fixture[9],
                    "subscribed": fixture[10]
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
                    "away_team_id": fixture[8],
                    "match_id": fixture[9],
                    "subscribed": fixture[10]
                }
                
            if competition_id is None:
                fixture_data["default_competition_ids"] = default_competition_ids
        
            result.append(fixture_data)

        return result

    def set_fav_team_matches_as_subscribed(favorite_team_id,reversed = 0):
        Queries.fav_team_id = favorite_team_id
        subscribed_value = 'No' if reversed == 1 else 'Yes'

        query = """
            UPDATE matches
            SET subscribed = %s
            WHERE home_team_id = %s OR away_team_id = %s
        """
    
        cursor.execute(query, (subscribed_value, favorite_team_id, favorite_team_id))
        db.commit()
        
    def toggle_match_as_subscribed(match_id, new_status):
        query = """
            UPDATE matches
            SET subscribed = %s
            WHERE match_id =%s
        """
        cursor.execute(query, (new_status,match_id))
        db.commit()
        print(match_id, new_status)
        
    def get_subscribed_matches(last=2, next=3):
        query = QueryTexts.subscribed_matches_query

        cursor.execute(query, (last, next))
        matches = cursor.fetchall()

        result = []
        for row in matches:
            if row[6] == 2001:
               competition_name = "UCL"
            elif row[6] == 2021:
                competition_name = "EPL"
            elif row[6] == 2015:
                competition_name = "Ligue 1"
            elif row[6] == 2014:
                competition_name = "LaLiga"
            elif row[6] == 2002:
                competition_name = "Bundesliga"
            elif row[6] == 2019:
                competition_name = "Serie A"
                
            appended_matchday = f"{competition_name} R{row[1]}"
            fixture_data = {
                "match_date": row[0],
                "matchday": appended_matchday,
                "home_team": row[2],
                "away_team": row[3],
                "home_score": row[4],
                "away_score": row[5],
                "competition_id": row[6], 
                "match_id": row[7],
                "home_team_id": row[8],
                "away_team_id": row[9],
                "subscribed": row[10]
            }
            result.append(fixture_data)

        return result

    def get_home_matches():
        
        matches = Queries.get_subscribed_matches()
        current_date = datetime.utcnow()
        matches_to_show = [] 
        unique_ids = set()
        
        for match in matches:
            match_date = match["match_date"]
            if match_date < current_date and len(matches_to_show) == 0:
                matches_to_show.append(match) 
                unique_ids.add(match["match_id"])
            elif match_date >= current_date:
                matches_to_show.append(match)
                unique_ids.add(match["match_id"])
                break

        comp_ids = [2001, 2021, 2014, 2002, 2019, 2015]
        for comp_id in comp_ids:
            hot_match = Queries.get_comp_recent_hot_match(comp_id)
            if hot_match is None:
                continue
            elif hot_match["match_id"] not in unique_ids:
                matches_to_show.append(hot_match)
                unique_ids.add(match["match_id"])             

        result = []
        for match in matches_to_show:
            competition_id = match["competition_id"]
            if competition_id == 2001:
                competition_name = "UCL"
            elif competition_id == 2021:
                competition_name = "EPL"
            elif competition_id == 2015:
                competition_name = "Ligue 1"
            elif competition_id == 2014:
                competition_name = "LaLiga"
            elif competition_id == 2002:
                competition_name = "Bundesliga"
            elif competition_id == 2019:
                competition_name = "Serie A"
            else:
                competition_name = "Unknown"

            if str(match['matchday'])[0].isdigit():
                appended_matchday = f"{competition_name} R{match['matchday']}"
            else:
                appended_matchday = match['matchday']

            fixture_data = {
                "match_date": match["match_date"],
                "matchday": appended_matchday,
                "home_team": match["home_team"],
                "away_team": match["away_team"],
                "home_score": match["home_score"],
                "away_score": match["away_score"],
                "competition_id": match["competition_id"],
                "match_id": match["match_id"],
                "home_team_id": match["home_team_id"],
                "away_team_id": match["away_team_id"],
                "subscribed": match["subscribed"]
            }
            result.append(fixture_data)

        return result
    
    def get_player_stats(competition_id):
        result = {
            "top_scorers": [],
            "top_assist_providers": [],
            "top_yellow_card_recipients": [],
            "top_red_card_recipients": [],
            "top_clean_sheet_providers": []
        }

        query_top_scorers = QueryTexts.query_top_scorers
        cursor.execute(query_top_scorers, (competition_id,))
        top_scorers = cursor.fetchall()

        for player in top_scorers:
            result["top_scorers"].append({
                "player_name": player[0],
                "total_goals": player[2],
                "team_name": player[1]
            })

        query_top_assists = QueryTexts.query_top_assists
        cursor.execute(query_top_assists, (competition_id,))
        top_assist_providers = cursor.fetchall()

        for player in top_assist_providers:
            result["top_assist_providers"].append({
                "player_name": player[0],
                "total_assists": player[2],
                "team_name": player[1]
            })

        query_top_yellow_cards = QueryTexts.query_top_yellow_cards
        cursor.execute(query_top_yellow_cards, (competition_id,))
        top_yellow_card_recipients = cursor.fetchall()

        for player in top_yellow_card_recipients:
            result["top_yellow_card_recipients"].append({
                "player_name": player[0],
                "total_yellow_cards": player[2],
                "team_name": player[1]
            })

        query_top_red_cards = QueryTexts.query_top_red_cards
        cursor.execute(query_top_red_cards, (competition_id,))
        top_red_card_recipients = cursor.fetchall()

        for player in top_red_card_recipients:
            result["top_red_card_recipients"].append({
                "player_name": player[0],
                "total_red_cards": player[2],
                "team_name": player[1]
            })

        query_top_clean_sheets = QueryTexts.query_top_clean_sheets
        cursor.execute(query_top_clean_sheets, (competition_id,))
        top_clean_sheet_providers = cursor.fetchall()

        for player in top_clean_sheet_providers:
            result["top_clean_sheet_providers"].append({
                "player_name": player[0],
                "total_clean_sheets": player[2],
                "team_name": player[1]
            })

        return result
    
    def get_comp_next_match(comp_id):
        query = QueryTexts.comp_next_match_query
        cursor.execute(query, (datetime.now(),comp_id))
        fixture = cursor.fetchone()
        if fixture:
            fixture_data = {
                "match_id": fixture[0],
                "home_team": fixture[1],
                "away_team": fixture[2],
                "home_score": fixture[3],  
                "away_score": fixture[4],  
                "match_date": fixture[5],  
                "competition": fixture[6],  
                "matchday": fixture[7],
                "home_team_id": fixture[8],
                "away_team_id": fixture[9],
                "subscribed": fixture[10],
                "competition_id": fixture[11]
            }
            return fixture_data
        else:
            print("No Next match found for " + str(comp_id))
            return None
     
    def get_comp_prev_match(comp_id):
        query = QueryTexts.comp_previous_match_query
        cursor.execute(query, (comp_id,))
        fixture = cursor.fetchone()
        if fixture:
            fixture_data = {
                "match_id": fixture[0],
                "home_team": fixture[1],
                "away_team": fixture[2],
                "home_score": fixture[3] ,  
                "away_score": fixture[4] ,  
                "match_date": fixture[5],  
                "competition": fixture[6],  
                "matchday": fixture[7],
                "home_team_id": fixture[8],
                "away_team_id": fixture[9],
                "subscribed": fixture[10],
                "competition_id":fixture[11]
            }
            return fixture_data
        else:
            print("No Previous match found for " + str(comp_id))
            return None
        
    def get_comp_recent_hot_match(comp_id):
        fixtures = Queries.get_fixtures(comp_id)
        team_ranks = Queries.get_competition_standings(comp_id)
        ranks_map = {team["team_id"]: team["points"] for team in team_ranks}
        highest_avg = 0
        recent_hot_match = None
        # print(comp_id)
        for fixture in fixtures:
            home_team_rank = ranks_map.get(fixture["home_team_id"], None)
            away_team_rank = ranks_map.get(fixture["away_team_id"], None)
            if home_team_rank is None or away_team_rank is None:
                continue
            avg_rank = (home_team_rank + away_team_rank) / 2
            if avg_rank > highest_avg:
                highest_avg = avg_rank
                recent_hot_match = fixture
                recent_hot_match["competition_id"] = comp_id

        return recent_hot_match

            
        
            