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

        sub_stack = qtw.QStackedWidget(main_window)

        # Add subtabs with match data from matches.py
        sub_stack.addWidget(UILoader.create_sub_tab_match(get_main_matches()))  # Main
        sub_stack.addWidget(UILoader.create_sub_tab_match(get_epl_matches()))   # EPL
        sub_stack.addWidget(UILoader.create_sub_tab_match(get_la_liga_matches()))  # La Liga
        sub_stack.addWidget(UILoader.create_sub_tab_match(get_bundesliga_matches()))  # Bundesliga
        sub_stack.addWidget(UILoader.create_sub_tab_match(get_serie_a_matches()))  # Serie A
        sub_stack.addWidget(UILoader.create_sub_tab_match(get_ligue_1_matches()))  # Ligue 1

        main_layout.addWidget(sub_stack)

        # Subtab buttons
        sub_tab_bar_layout = qtw.QHBoxLayout()
        buttons = ["Main", "EPL", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]
        for i, name in enumerate(buttons):
            btn = qtw.QPushButton(name)
            btn.setStyleSheet("QPushButton { text-align: center; }")  
            btn.clicked.connect(lambda _, idx=i: UILoader.update_sub_tab_buttons(sub_tab_bar_layout, idx, btn, sub_stack))
            sub_tab_bar_layout.addWidget(btn)

        main_layout.insertLayout(0, sub_tab_bar_layout)
        match_tab.setLayout(main_layout)

        # Set default selection for match sub-tab (Main)
        UILoader.update_sub_tab_buttons(sub_tab_bar_layout, 0, sub_tab_bar_layout.itemAt(0).widget(), sub_stack)
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

        sub_stack = qtw.QStackedWidget(main_window)

        sub_stack.addWidget(UILoader.create_sub_tab_stats(get_ucl_stats()))  
        sub_stack.addWidget(UILoader.create_sub_tab_stats(get_epl_stats()))  # EPL
        sub_stack.addWidget(UILoader.create_sub_tab_stats(get_laliga_stats()))  # La Liga
        sub_stack.addWidget(UILoader.create_sub_tab_stats(get_bundesliga_stats()))  # Bundesliga
        sub_stack.addWidget(UILoader.create_sub_tab_stats(get_serie_a_stats()))  # Serie A
        sub_stack.addWidget(UILoader.create_sub_tab_stats(get_ligue_1_stats()))  # Ligue 1

        main_layout.addWidget(sub_stack)

        sub_tab_bar_layout = qtw.QHBoxLayout()
        buttons = ["UCL", "EPL", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]
        for i, name in enumerate(buttons):
            btn = qtw.QPushButton(name)
            btn.setStyleSheet("QPushButton { text-align: center; }")  
            btn.clicked.connect(lambda _, idx=i: UILoader.update_sub_tab_buttons(sub_tab_bar_layout, idx, btn, sub_stack))
            sub_tab_bar_layout.addWidget(btn)

        main_layout.insertLayout(0, sub_tab_bar_layout)
        stats_tab.setLayout(main_layout)

        # Set default selection for stats sub-tab (UCL)
        UILoader.update_sub_tab_buttons(sub_tab_bar_layout, 0, sub_tab_bar_layout.itemAt(0).widget(), sub_stack)
        return stats_tab
    


    # Function to create the favorite tab content, called only when the tab is clicked
    @staticmethod
    def load_favorite_tab_content(favorite_tab):
        layout = favorite_tab.layout()

        # Check if favorite team is set
        favorite_team = UILoader.get_favorite_team()
        if not favorite_team:
            # If no favorite team, prompt user to set it
            UILoader.prompt_set_favorite_team()
            favorite_team = UILoader.get_favorite_team()  # Reload after setting
        else:
            # If favorite team exists, fetch and display stats
            #layout.addWidget(qtw.QLabel(f"Favorite Team: {favorite_team}"))
            print(f"Favorite team is: {favorite_team}")
            # Here you could add code to fetch stats for the favorite team
            # Example (commented out):
            # team_stats = get_team_stats(favorite_team)  # Function to fetch stats by team
            # if team_stats:
            #     for stat in team_stats:
            #         layout.addWidget(qtw.QLabel(f"{stat['description']}: {stat['value']}"))
            # else:
            #     layout.addWidget(qtw.QLabel("No stats available"))


    # Create Favorite tab (basic structure)
    @staticmethod
    def create_favorite_tab(main_window):
        favorite_tab = qtw.QWidget()
        layout = qtw.QVBoxLayout()
        favorite_tab.setLayout(layout)

        return favorite_tab

    # Functions for favorite team management (unchanged)
    @staticmethod
    def get_favorite_team():
        if os.path.exists(FAVORITE_TEAM_FILE):
            with open(FAVORITE_TEAM_FILE, 'r') as f:
                data = json.load(f)
                return data.get("team_name", None)
        return None

    @staticmethod
    def set_favorite_team(team_name):
        with open(FAVORITE_TEAM_FILE, 'w') as f:
            json.dump({"team_name": team_name}, f)
            print(f"Favorite team is: {team_name}")

    @staticmethod
    def prompt_set_favorite_team():
        dialog = qtw.QDialog()
        dialog.setWindowTitle("Set Favorite Team")
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



       
