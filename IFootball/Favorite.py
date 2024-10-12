import json
import os
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from Queries import Queries

FAVORITE_TEAM_FILE = "favorite_team.json"

class Favorite:
    
    @staticmethod
    def get_favorite_team():
        if os.path.exists(FAVORITE_TEAM_FILE):
            with open(FAVORITE_TEAM_FILE, 'r') as f:
                data = json.load(f)
                short_name = data.get("short_name", None)
                team_id = data.get("team_id", None)
                return short_name, team_id  
        return None, None

    @staticmethod
    def set_favorite_team(short_name):
        # Get team ID from the database
        team_id = Queries.get_team_id_by_name(short_name)
    
        if team_id:
            with open(FAVORITE_TEAM_FILE, 'w') as f:
                json.dump({"short_name": short_name, "team_id": team_id}, f)
                print(f"Favorite team set: {short_name} (ID: {team_id})")
        else:
            print(f"Team {short_name} not found in the database.")

    @staticmethod
    def prompt_set_favorite_team(main_window):
        dialog = qtw.QDialog(main_window)  # Set main_window as the parent to center the dialog
        dialog.setWindowTitle("Set Favorite Team")
    
        # Remove the "?" sign by adjusting the window flags
        dialog.setWindowFlags(dialog.windowFlags() & ~qtc.Qt.WindowContextHelpButtonHint)
        dialog.setGeometry(300, 100, 500, 800)
        dialog.setLayout(qtw.QVBoxLayout())

        label = qtw.QLabel("Please start typing your favorite team:")
        dialog.layout().addWidget(label)

        # Fetch teams from the database
        teams = Queries.fetch_teams_from_database()  # Function to retrieve all team names from the DB
    
        # Create an input field with auto-completion for team names
        team_input = qtw.QLineEdit()
        completer = qtw.QCompleter(teams)  # Create a completer with the team list
        completer.setCaseSensitivity(qtc.Qt.CaseInsensitive)  # Make auto-completion case insensitive
        team_input.setCompleter(completer)
        dialog.layout().addWidget(team_input)

        # Ok button
        ok_button = qtw.QPushButton("OK")
        ok_button.clicked.connect(lambda: Favorite.set_favorite_team(team_input.text()) or dialog.accept())
        dialog.layout().addWidget(ok_button)

        dialog.exec_()

    @staticmethod
    def load_favorite_tab_content():
        # Check if favorite team is set
        favorite_team, favorite_team_id = Favorite.get_favorite_team()

        # If no favorite team is set, prompt user to set it
        if not favorite_team:
            Favorite.prompt_set_favorite_team(None)  
            favorite_team, favorite_team_id = Favorite.get_favorite_team()

        # Initialize last and next match variables
        last_matches = []
        next_matches = []

        if favorite_team:
            last_matches = Queries.get_last_matches(favorite_team_id)
            next_matches = Queries.get_next_matches(favorite_team_id)

        # Return the necessary data to be displayed
        return favorite_team, favorite_team_id, last_matches, next_matches

    @staticmethod
    def create_fixture_layout(favorite_team, favorite_team_id, last_matches, next_matches):
        """
        Create the layout for the fixture tab with favorite team details, last 2 matches, and next 2 matches.
        Returns the created layout.
        """
        fixture_layout = qtw.QVBoxLayout()

        # Add favorite team information
        if favorite_team:
            fixture_layout.addWidget(qtw.QLabel(f"Favorite Team: {favorite_team} (ID: {favorite_team_id})"))

            # Display last 2 matches
            fixture_layout.addWidget(qtw.QLabel("Previous Matches:"))
            if last_matches:
                for match in last_matches:
                    fixture_layout.addWidget(qtw.QLabel(
                        f"{match['competition']} R{match['matchday']}: "
                        f"{match['team1']} {match['score1']} - {match['score2']} {match['team2']} on {match['date']}"))
            else:
                fixture_layout.addWidget(qtw.QLabel("No recent matches available"))

            # Display next 2 matches
            fixture_layout.addWidget(qtw.QLabel("Next Matches:"))
            if next_matches:
                for match in next_matches:
                    fixture_layout.addWidget(qtw.QLabel(
                        f"{match['competition']} R{match['matchday']}: "
                        f"{match['team1']} vs {match['team2']} on {match['date']}"))
            else:
                fixture_layout.addWidget(qtw.QLabel("No upcoming matches available"))
        else:
            fixture_layout.addWidget(qtw.QLabel("No favorite team set."))

        # Add stretch to the layout
        fixture_layout.addStretch()
        return fixture_layout

    @staticmethod
    def create_stats_layout(favorite_team, favorite_team_id):
        """
        Create the layout for the stats tab with favorite team statistics.
        Returns the created layout.
        """
        stats_layout = qtw.QVBoxLayout()

        if favorite_team_id:
            team_stats = Queries.get_team_stats_in_fav(favorite_team_id)

            # Add team statistics
            stats_layout.addWidget(qtw.QLabel(f"Team Stats for {favorite_team}:"))

            if team_stats:
                for index, stat in enumerate(team_stats):
                    stats_layout.addWidget(qtw.QLabel(f"Competition: {stat['competition']}"))
                    stats_layout.addWidget(qtw.QLabel(f"Matches Played: {stat['total_matches']}"))
                    stats_layout.addWidget(qtw.QLabel(f"Wins: {stat['wins']}"))
                    stats_layout.addWidget(qtw.QLabel(f"Draws: {stat['draws']}"))
                    stats_layout.addWidget(qtw.QLabel(f"Losses: {stat['losses']}"))
                    stats_layout.addWidget(qtw.QLabel(f"Goals Scored: {stat['goals_scored']}"))
                    stats_layout.addWidget(qtw.QLabel(f"Goals Conceded: {stat['goals_conceded']}"))
                    stats_layout.addWidget(qtw.QLabel(f"Goal Difference: {stat['goal_difference']}"))

                    if stat['biggest_win']:
                        stats_layout.addWidget(qtw.QLabel("Biggest Win:"))
                        biggest_win = stat['biggest_win']
                        stats_layout.addWidget(qtw.QLabel(
                            f"{biggest_win['team_goals']} - {biggest_win['opponent_goals']} "
                            f"against {biggest_win['opponent']} on {biggest_win['date']} R{biggest_win['matchday']}"))
                    else:
                        stats_layout.addWidget(qtw.QLabel("No biggest wins available."))

                    if index < len(team_stats) - 1:
                        stats_layout.addWidget(qtw.QLabel("-" * 70))
            else:
                stats_layout.addWidget(qtw.QLabel("No stats available for this team."))
        else:
            stats_layout.addWidget(qtw.QLabel("No favorite team set for stats."))

        stats_layout.addStretch()
        return stats_layout