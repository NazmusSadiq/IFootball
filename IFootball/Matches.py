from Queries import Queries
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

class Matches:
    def get_league_matches(competition_id):
        # Logic to get main matches (mock data for now)
        return [
            {"team1": "Team A", "team2": "Team B", "date": "2024-10-10"},
            {"team1": "Team C", "team2": "Team D", "date": "2024-10-12"}
        ]

    def get_main_matches():
        # Logic to get EPL matches (mock data for now)
        return [
            {"team1": "Arsenal", "team2": "Liverpool", "date": "2024-10-15"},
            {"team1": "Chelsea", "team2": "Man Utd", "date": "2024-10-17"}
        ]
    
    def get_subscribed_matches():
        # Logic to get EPL matches (mock data for now)
        return [
            {"team1": "Arsenal", "team2": "Liverpool", "date": "2024-10-15"},
            {"team1": "Chelsea", "team2": "Man Utd", "date": "2024-10-17"}
        ]

    