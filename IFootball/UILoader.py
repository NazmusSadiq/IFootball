import json
import os
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from Matches import get_main_matches, get_epl_matches, get_la_liga_matches, get_bundesliga_matches, get_serie_a_matches, get_ligue_1_matches
from Stats import Stats
from Queries import Queries
from Favorite import Favorite

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
        button.setIconSize(qtc.QSize(24, 24))
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

        if stats:        
            column_widths = {
                "Team": 200,"P": 50,"W": 50,"D": 50,"L": 50,"F/A": 100,"Pts": 50
            }
    
            # Create a grid layout for the headings
            header_layout = qtw.QGridLayout()

            # Add headers with fixed column positions and widths
            team_header = qtw.QLabel("Team")
            team_header.setFixedWidth(column_widths["Team"])
            header_layout.addWidget(team_header, 0, 0, alignment=qtc.Qt.AlignLeft)

            p_header = qtw.QLabel("P")
            p_header.setFixedWidth(column_widths["P"])
            header_layout.addWidget(p_header, 0, 1, alignment=qtc.Qt.AlignCenter)

            w_header = qtw.QLabel("W")
            w_header.setFixedWidth(column_widths["W"])
            header_layout.addWidget(w_header, 0, 2, alignment=qtc.Qt.AlignCenter)

            d_header = qtw.QLabel("D")
            d_header.setFixedWidth(column_widths["D"])
            header_layout.addWidget(d_header, 0, 3, alignment=qtc.Qt.AlignCenter)

            l_header = qtw.QLabel("L")
            l_header.setFixedWidth(column_widths["L"])
            header_layout.addWidget(l_header, 0, 4, alignment=qtc.Qt.AlignCenter)

            fa_header = qtw.QLabel("F/A")
            fa_header.setFixedWidth(column_widths["F/A"])
            header_layout.addWidget(fa_header, 0, 5, alignment=qtc.Qt.AlignCenter)

            pts_header = qtw.QLabel("Pts")
            pts_header.setFixedWidth(column_widths["Pts"])
            header_layout.addWidget(pts_header, 0, 6, alignment=qtc.Qt.AlignCenter)

            # Add header layout to main layout
            layout.addLayout(header_layout)

            # Add spacing for better visibility
            layout.addSpacing(10)

            team_rank = 1
            for stat in stats:
                if isinstance(stat, dict):
                    # Create a grid layout for each team's data
                    team_layout = qtw.QGridLayout()

                    # Add team rank and name with fixed width
                    team_label = qtw.QLabel(f"{team_rank}. {stat['team_name']}")
                    team_label.setFixedWidth(column_widths["Team"])
                    team_layout.addWidget(team_label, 0, 0, alignment=qtc.Qt.AlignLeft)

                    # Add played matches with fixed width
                    played_label = qtw.QLabel(f"{stat['wins'] + stat['losses'] + stat['draws']}")
                    played_label.setFixedWidth(column_widths["P"])
                    team_layout.addWidget(played_label, 0, 1, alignment=qtc.Qt.AlignCenter)

                    # Add wins with fixed width
                    wins_label = qtw.QLabel(f"{stat['wins']}")
                    wins_label.setFixedWidth(column_widths["W"])
                    team_layout.addWidget(wins_label, 0, 2, alignment=qtc.Qt.AlignCenter)

                    # Add draws with fixed width
                    draws_label = qtw.QLabel(f"{stat['draws']}")
                    draws_label.setFixedWidth(column_widths["D"])
                    team_layout.addWidget(draws_label, 0, 3, alignment=qtc.Qt.AlignCenter)

                    # Add losses with fixed width
                    losses_label = qtw.QLabel(f"{stat['losses']}")
                    losses_label.setFixedWidth(column_widths["L"])
                    team_layout.addWidget(losses_label, 0, 4, alignment=qtc.Qt.AlignCenter)

                    # Add goals scored/conceded with fixed width
                    fa_label = qtw.QLabel(f"{stat['goals_scored']} / {stat['goals_conceded']}")
                    fa_label.setFixedWidth(column_widths["F/A"])
                    team_layout.addWidget(fa_label, 0, 5, alignment=qtc.Qt.AlignCenter)

                    # Add points with fixed width
                    points_label = qtw.QLabel(f"{stat['points']}")
                    points_label.setFixedWidth(column_widths["Pts"])
                    team_layout.addWidget(points_label, 0, 6, alignment=qtc.Qt.AlignCenter)

                    # Add the team layout to the main layout
                    layout.addLayout(team_layout)

                    team_rank += 1

                else:
                    stat_label = qtw.QLabel("Invalid stat format")
                    layout.addWidget(stat_label)
        else:
            no_stat_label = qtw.QLabel("No stats available")
            layout.addWidget(no_stat_label)

        # Add a spacer to ensure proper spacing
        layout.addStretch()

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
        sub_stack.addWidget(UILoader.create_sub_tab_stats(Stats.get_competition_standings(2001)))  # UCL
        sub_stack.addWidget(UILoader.create_sub_tab_stats(Stats.get_competition_standings(2021)))  # EPL
        sub_stack.addWidget(UILoader.create_sub_tab_stats(Stats.get_competition_standings(2014)))  # La Liga
        sub_stack.addWidget(UILoader.create_sub_tab_stats(Stats.get_competition_standings(2002)))  # Bundesliga
        sub_stack.addWidget(UILoader.create_sub_tab_stats(Stats.get_competition_standings(2019)))  # Serie A
        sub_stack.addWidget(UILoader.create_sub_tab_stats(Stats.get_competition_standings(2015)))  # Ligue 1

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

        # Load the favorite team information
        favorite_team, favorite_team_id, last_matches, next_matches = Favorite.load_favorite_tab_content()

        # Create the Fixture and Stats layouts
        fixture_layout = Favorite.create_fixture_layout(favorite_team, favorite_team_id, last_matches, next_matches)
        stats_layout = Favorite.create_stats_layout(favorite_team, favorite_team_id)

        # Create the Fixture and Stats tabs
        fixture_tab = qtw.QWidget()
        fixture_tab.setLayout(fixture_layout)

        stats_tab = qtw.QWidget()
        stats_tab.setLayout(stats_layout)

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
            btn.clicked.connect(lambda _, i=i: sub_stack.setCurrentIndex(i))
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



    


   

    
       
