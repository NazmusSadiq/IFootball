import json
import os
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as QtCore
from Matches import get_main_matches, get_epl_matches, get_la_liga_matches, get_bundesliga_matches, get_serie_a_matches, get_ligue_1_matches
from Stats import get_serie_a_stats, get_ucl_stats, get_epl_stats, get_laliga_stats, get_bundesliga_stats, get_serie_a_stats, get_ligue_1_stats
from Queries import Queries

FAVORITE_TEAM_FILE = "favorite_team.json"

class UILoader:
    @staticmethod
    def clear_section(layout):
        section_name="common_section"
        for i in reversed(range(layout.count())):
            widget = layout.itemAt(i).widget()
            if widget and widget.objectName() == section_name:
                layout.removeWidget(widget)
                widget.deleteLater()

    # Function to create bottom tabs with icons
    @staticmethod
    def create_bottom_tab(main_window, name, icon_path_default, icon_path_selected):
        button = qtw.QPushButton(name)
        button.icon_path_default = icon_path_default
        button.icon_path_selected = icon_path_selected

        button.setIcon(qtg.QIcon(icon_path_default))
        button.setIconSize(QtCore.QSize(24, 24))
        button.setStyleSheet("QPushButton { text-align: center; color: grey; }")

        button.clicked.connect(lambda: main_window.switch_tab(button))
        return button

    # Function to create content for each sub-tab with match data
    @staticmethod
    def create_sub_tab_match(matches):
        widget = qtw.QWidget()
        layout = qtw.QVBoxLayout()

        # Display match data
        if matches:
            for match in matches:
                match_label = qtw.QLabel(f"{match['team1']} vs {match['team2']} - {match['date']}")
                layout.addWidget(match_label)
        else:
            no_match_label = qtw.QLabel("No matches available")
            layout.addWidget(no_match_label)

        # Add a spacer to ensure proper spacing
        layout.addStretch()  # This adds space below the labels

        widget.setLayout(layout)
        return widget

    # Function to create content for each sub-tab with stats data
    @staticmethod
    def create_sub_tab_stats(stats):
        widget = qtw.QWidget()
        layout = qtw.QVBoxLayout()

        # Display stats data
        if stats:
          for stat in stats:
                if isinstance(stat, dict):
                    stat_label = qtw.QLabel(f"{stat['team']} - Points: {stat['points']}, Goals: {stat['goals']}, Wins: {stat['wins']}")
                elif isinstance(stat, str):
                    stat_label = qtw.QLabel(stat)  # Directly display the string if it's a string
                else:
                    stat_label = qtw.QLabel("Invalid stat format")
                layout.addWidget(stat_label)
        else:
            no_stat_label = qtw.QLabel("No stats available")
            layout.addWidget(no_stat_label)

        # Add a spacer to ensure proper spacing
        layout.addStretch()  # This adds space below the labels

        widget.setLayout(layout)
        return widget


    
    # Create Home tab content
    @staticmethod
    def create_home_tab():
        home_tab = qtw.QWidget()
        layout = qtw.QVBoxLayout()
        home_tab.setLayout(layout)
        return home_tab

    # Create Match tab content with subtabs
    @staticmethod
    def create_match_tab(main_window):
        match_tab = qtw.QWidget()
        main_layout = qtw.QVBoxLayout()

        # Clear previous content if it exists
        UILoader.clear_section(main_layout)

        # Create a new section widget for match data
        section_widget = qtw.QWidget()
        section_layout = qtw.QVBoxLayout(section_widget)
        section_widget.setObjectName("common_section")

        # Create a stacked widget to hold the different sub-tabs
        sub_stack = qtw.QStackedWidget(main_window)

        # Add subtabs with match data from matches.py
        sub_stack.addWidget(UILoader.create_sub_tab_match(get_main_matches()))  # Main
        sub_stack.addWidget(UILoader.create_sub_tab_match(get_epl_matches()))   # EPL
        sub_stack.addWidget(UILoader.create_sub_tab_match(get_la_liga_matches()))  # La Liga
        sub_stack.addWidget(UILoader.create_sub_tab_match(get_bundesliga_matches()))  # Bundesliga
        sub_stack.addWidget(UILoader.create_sub_tab_match(get_serie_a_matches()))  # Serie A
        sub_stack.addWidget(UILoader.create_sub_tab_match(get_ligue_1_matches()))  # Ligue 1

        section_layout.addWidget(sub_stack)
        main_layout.addWidget(section_widget)

        # Subtab buttons
        sub_tab_bar_layout = qtw.QHBoxLayout()
        buttons = ["Main", "EPL", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]
        for i, name in enumerate(buttons):
            btn = qtw.QPushButton(name)
            btn.setStyleSheet("QPushButton { text-align: center; }")  
            btn.clicked.connect(lambda _, idx=i: UILoader.update_sub_tab_buttons(sub_tab_bar_layout, idx, btn, sub_stack))
            sub_tab_bar_layout.addWidget(btn)

        # Insert the sub-tab buttons at the top of the layout
        main_layout.insertLayout(0, sub_tab_bar_layout)

        # Set the default selection for the match sub-tab (Main)
        UILoader.update_sub_tab_buttons(sub_tab_bar_layout, 0, sub_tab_bar_layout.itemAt(0).widget(), sub_stack)

        match_tab.setLayout(main_layout)

        return match_tab



    @staticmethod
    def update_sub_tab_buttons(layout, active_index, active_button, sub_stack):
        for i in range(layout.count()):
            button = layout.itemAt(i).widget()
            if i == active_index:
                button.setStyleSheet("QPushButton { text-align: center; font-weight: bold; }")  
            else:
                button.setStyleSheet("QPushButton { text-align: center; }") 
        sub_stack.setCurrentIndex(active_index)

    # Create Stats tab content with different subtabs
    @staticmethod
    def create_stats_tab(main_window):
        stats_tab = qtw.QWidget()
        main_layout = qtw.QVBoxLayout()

        # Clear previous content if it exists
        UILoader.clear_section(main_layout)

        # Create a new section widget for stats data
        section_widget = qtw.QWidget()
        section_layout = qtw.QVBoxLayout(section_widget)
        section_widget.setObjectName("common_section")

        # Create a stacked widget to hold the different sub-tabs
        sub_stack = qtw.QStackedWidget(main_window)

        # Add subtabs with stats data
        sub_stack.addWidget(UILoader.create_sub_tab_stats(get_ucl_stats()))  # UCL
        sub_stack.addWidget(UILoader.create_sub_tab_stats(get_epl_stats()))  # EPL
        sub_stack.addWidget(UILoader.create_sub_tab_stats(get_laliga_stats()))  # La Liga
        sub_stack.addWidget(UILoader.create_sub_tab_stats(get_bundesliga_stats()))  # Bundesliga
        sub_stack.addWidget(UILoader.create_sub_tab_stats(get_serie_a_stats()))  # Serie A
        sub_stack.addWidget(UILoader.create_sub_tab_stats(get_ligue_1_stats()))  # Ligue 1

        section_layout.addWidget(sub_stack)
        main_layout.addWidget(section_widget)

        # Subtab buttons
        sub_tab_bar_layout = qtw.QHBoxLayout()
        buttons = ["UCL", "EPL", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]
        for i, name in enumerate(buttons):
            btn = qtw.QPushButton(name)
            btn.setStyleSheet("QPushButton { text-align: center; }")
            btn.clicked.connect(lambda _, idx=i: UILoader.update_sub_tab_buttons(sub_tab_bar_layout, idx, btn, sub_stack))
            sub_tab_bar_layout.addWidget(btn)

        # Insert the sub-tab buttons at the top of the layout
        main_layout.insertLayout(0, sub_tab_bar_layout)

        # Set the default selection for the stats sub-tab (UCL)
        UILoader.update_sub_tab_buttons(sub_tab_bar_layout, 0, sub_tab_bar_layout.itemAt(0).widget(), sub_stack)

        stats_tab.setLayout(main_layout)

        return stats_tab


    
    @staticmethod
    def create_favorite_tab(main_window):
        # Create the favorite tab widget and layout
        favorite_tab = qtw.QWidget()
        main_layout = qtw.QVBoxLayout()

        # Clear previous content if it exists
        UILoader.clear_section(main_layout)

        # Create a new section widget for favorite team data
        section_widget = qtw.QWidget()
        section_layout = qtw.QVBoxLayout(section_widget)
        section_widget.setObjectName("common_section")

        # Create a stacked widget to hold the different sub-tabs (Fixture, Stats)
        sub_stack = qtw.QStackedWidget(main_window)

        # Create the Fixture and Stats tabs
        fixture_tab = qtw.QWidget()
        fixture_layout = qtw.QVBoxLayout(fixture_tab)

        stats_tab = qtw.QWidget()
        stats_layout = qtw.QVBoxLayout(stats_tab)

        # Load the favorite team content
        favorite_team, favorite_team_id, last_matches, next_matches = UILoader.load_favorite_tab_content()

        # Add favorite team information to the fixture layout
        if favorite_team:
            fixture_layout.addWidget(qtw.QLabel(f"Favorite Team: {favorite_team} (ID: {favorite_team_id})"))

            # Display last 2 matches
            fixture_layout.addWidget(qtw.QLabel("Previous Matches:"))
            if last_matches:
                for match in last_matches:
                    fixture_layout.addWidget(qtw.QLabel(
                        f"{match['competition']} R{match['matchday']}: "
                        f"{match['team1']} {match['score1']} - {match['score2']} {match['team2']} on {match['date']}"
                    ))
            else:
                fixture_layout.addWidget(qtw.QLabel("No recent matches available"))

            # Display next 2 matches
            fixture_layout.addWidget(qtw.QLabel("Next Matches:"))
            if next_matches:
                for match in next_matches:
                    fixture_layout.addWidget(qtw.QLabel(
                        f"{match['competition']} R{match['matchday']}: "
                        f"{match['team1']} vs {match['team2']} on {match['date']}"
                    ))
            else:
                fixture_layout.addWidget(qtw.QLabel("No upcoming matches available"))
        else:
            fixture_layout.addWidget(qtw.QLabel("No favorite team set."))

        # Add stretch to the fixture layout
        fixture_layout.addStretch()

        # Load the favorite team's statistics using the get_team_stats function
        if favorite_team_id:
            team_stats = Queries.get_team_stats(favorite_team_id)

            # Add team statistics to the stats layout
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

                    # Display the biggest win for the competition
                    if stat['biggest_win']:
                        stats_layout.addWidget(qtw.QLabel("Biggest Win:"))
                        biggest_win = stat['biggest_win']
                        stats_layout.addWidget(qtw.QLabel(
                            f"{biggest_win['team_goals']} - {biggest_win['opponent_goals']} "
                            f"against {biggest_win['opponent']} on {biggest_win['date']} R{biggest_win['matchday']}"
                        ))
                    else:
                        stats_layout.addWidget(qtw.QLabel("No biggest wins available."))


                    # Add a separator only if it's not the last element
                    if index < len(team_stats) - 1:
                        stats_layout.addWidget(qtw.QLabel("-" * 70))  
            
            else:
                stats_layout.addWidget(qtw.QLabel("No stats available for this team."))

        else:
            stats_layout.addWidget(qtw.QLabel("No favorite team set for stats."))

        # Add stretch to the Stats layout
        stats_layout.addStretch()

        # Add the fixture and stats tabs to the stacked widget
        sub_stack.addWidget(fixture_tab)  # Fixture tab
        sub_stack.addWidget(stats_tab)    # Stats tab

        section_layout.addWidget(sub_stack)
        main_layout.addWidget(section_widget)

        # Subtab buttons
        sub_tab_bar_layout = qtw.QHBoxLayout()
        buttons = ["Fixture", "Stats"]
        for i, name in enumerate(buttons):
            btn = qtw.QPushButton(name)
            btn.setStyleSheet("QPushButton { text-align: center; }")
            btn.clicked.connect(lambda _, idx=i: UILoader.update_sub_tab_buttons(sub_tab_bar_layout, idx, btn, sub_stack))
            sub_tab_bar_layout.addWidget(btn)

        # Insert the sub-tab buttons at the top of the layout
        main_layout.insertLayout(0, sub_tab_bar_layout)

        # Set the default selection for the favorite tab (Fixture)
        UILoader.update_sub_tab_buttons(sub_tab_bar_layout, 0, sub_tab_bar_layout.itemAt(0).widget(), sub_stack)

        favorite_tab.setLayout(main_layout)

        return favorite_tab


    @staticmethod
    def update_sub_tab_buttons(layout, active_index, active_button, sub_stack):
        for i in range(layout.count()):
            button = layout.itemAt(i).widget()
            if i == active_index:
                button.setStyleSheet("QPushButton { text-align: center; font-weight: bold; }")
            else:
                button.setStyleSheet("QPushButton { text-align: center; }")
        sub_stack.setCurrentIndex(active_index)



    @staticmethod
    def load_favorite_tab_content():
        # Check if favorite team is set
        favorite_team, favorite_team_id = UILoader.get_favorite_team()

        # If no favorite team is set, prompt user to set it
        if not favorite_team:
            UILoader.prompt_set_favorite_team(None)  
            favorite_team, favorite_team_id = UILoader.get_favorite_team()

        # Initialize last and next match variables
        last_matches = []
        next_matches = []

        if favorite_team:
            last_matches = Queries.get_last_matches(favorite_team_id)
            next_matches = Queries.get_next_matches(favorite_team_id)

        # Return the necessary data to be displayed
        return favorite_team, favorite_team_id, last_matches, next_matches


    # Functions for favorite team management (unchanged)
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
        dialog.setWindowFlags(dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        dialog.setGeometry(300, 100, 500, 800)
        dialog.setLayout(qtw.QVBoxLayout())

        label = qtw.QLabel("Please start typing your favorite team:")
        dialog.layout().addWidget(label)

        # Fetch teams from the database
        teams = Queries.fetch_teams_from_database()  # Function to retrieve all team names from the DB
    
        # Create an input field with auto-completion for team names
        team_input = qtw.QLineEdit()
        completer = qtw.QCompleter(teams)  # Create a completer with the team list
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)  # Make auto-completion case insensitive
        team_input.setCompleter(completer)
        dialog.layout().addWidget(team_input)

        # Ok button
        ok_button = qtw.QPushButton("OK")
        ok_button.clicked.connect(lambda: UILoader.set_favorite_team(team_input.text()) or dialog.accept())
        dialog.layout().addWidget(ok_button)

        dialog.exec_()



       
