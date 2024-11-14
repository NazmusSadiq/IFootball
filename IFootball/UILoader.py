import json
import os
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from Matches import Matches
from Stats import Stats
from Queries import Queries
from Favorite import Favorite
from datetime import datetime

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

        if matches:
            # Create headers
            Matches.create_headers(layout)
            layout.addSpacing(10)
            if isinstance(matches, list):  # Team stats should be a list of dicts
                team_rank = 1
                for match in matches:
                    if isinstance(match, dict):
                        Matches.create_match_row(layout, match)          
                    else:
                        print(f"Unexpected stat format: {match}")
                        stat_label = qtw.QLabel("Invalid stat format")
                        layout.addWidget(stat_label)
            else:
                print(f"Unexpected stat structure for team stats: {match}")
        else:
            no_match_label = qtw.QLabel("No matches available")
            layout.addWidget(no_match_label)
            
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    # @staticmethod
    # def create_main_match_tab():
    #     match_tab = qtw.QWidget()
    #     main_layout = qtw.QVBoxLayout()
    
    #     UILoader.clear_section(main_layout)  # Clear previous content if any
    
    #     # Widget to hold all competitions in a vertical layout
    #     competitions_widget = qtw.QWidget()
    #     competitions_layout = qtw.QVBoxLayout(competitions_widget)
    
    #     # Define competition IDs and their names
    #     competitions = {
    #         2014: "La Liga",
    #         2001: "UCL",
    #         2021: "EPL",
    #         2002: "Bundesliga",
    #         2019: "Serie A",
    #         2015: "Ligue 1"
    #     }
    
    #     # Loop through competitions and add them to the layout
    #     for comp_id, comp_name in competitions.items():
    #         # Section header for the competition
    #         header = qtw.QLabel(f"<b>{comp_name}</b>")
    #         header.setAlignment(qtc.Qt.AlignCenter)
    #         header.setStyleSheet("font-size: 18px; margin: 10px 0;")
    
    #         competitions_layout.addWidget(header)
    
    #         # Fetch and display matches for the competition
    #         matches = Queries.get_league_matches(comp_id)
    #         competitions_layout.addWidget(UILoader.create_sub_tab_match(matches))
    
    #         # Add spacing between competitions
    #         competitions_layout.addSpacing(20)
    
    #     # Add a spacer to ensure proper alignment
    #     competitions_layout.addStretch()
        
    #     main_layout.addWidget(competitions_widget)
    
    #     match_tab.setLayout(main_layout)
    
    #     return match_tab
    


    # Create Home tab content with favorite team matches and news
    @staticmethod
    def create_home_tab():
        # Initialize the home tab widget and main layout
        home_tab = qtw.QWidget()
        main_layout = qtw.QVBoxLayout()
        
        # Create a scroll area to make the home tab scrollable
        scroll_area = qtw.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        
        # Container widget to hold the favorite matches and news sections
        content_widget = qtw.QWidget()
        content_layout = qtw.QVBoxLayout(content_widget)
        
        # Section 1: Favorite Team Matches
        favorite_team, favorite_team_id, last_matches, next_matches = Favorite.load_favorite_tab_content()
        
        # Display recent and upcoming matches using create_sub_tab_match
        favorite_matches_widget = UILoader.create_sub_tab_match(last_matches + next_matches)
        
        # Set up the favorite section widget and layout
        favorite_section_widget = qtw.QWidget()
        favorite_section_layout = qtw.QVBoxLayout(favorite_section_widget)
        favorite_section_label = qtw.QLabel("<b>Favorite Team Matches</b>")
        favorite_section_label.setAlignment(qtc.Qt.AlignCenter)
        
        # Add the label and the matches widget to the layout
        favorite_section_layout.addWidget(favorite_section_label)
        favorite_section_layout.addWidget(favorite_matches_widget)  # Use the widget directly
        favorite_section_layout.addStretch()
        
        # Add the favorite section to the main content layout
        content_layout.addWidget(favorite_section_widget)
        
        # Section 2: News
        news_layout = Favorite.create_news_layout(favorite_team)
        
        news_section_widget = qtw.QWidget()
        news_section_layout = qtw.QVBoxLayout(news_section_widget)
        news_section_label = qtw.QLabel("<b>News</b>")
        news_section_label.setAlignment(qtc.Qt.AlignCenter)
        news_section_layout.addWidget(news_section_label)
        news_section_layout.addLayout(news_layout)
        news_section_layout.addStretch()
        
        # Add the news section to a separate scroll area
        news_scroll_area = qtw.QScrollArea()
        news_scroll_area.setWidgetResizable(True)
        news_scroll_area.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAsNeeded)
        news_scroll_area.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        news_scroll_area.setWidget(news_section_widget)
        
        # Add the news scroll area to the main content layout
        content_layout.addWidget(news_scroll_area)
        
        # Add the content to the main scroll area
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Set the layout for the home tab
        home_tab.setLayout(main_layout)

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
        sub_stack.addWidget(UILoader.create_sub_tab_match(Queries.get_fixtures()))  # Main for now
        sub_stack.addWidget(UILoader.create_sub_tab_match(Queries.get_subscribed_matches()))  # Subscribed 
        sub_stack.addWidget(UILoader.create_sub_tab_match(Queries.get_fixtures(2001,2,4)))  # UCL
        sub_stack.addWidget(UILoader.create_sub_tab_match(Queries.get_fixtures(2021,2,4)))  # EPL
        sub_stack.addWidget(UILoader.create_sub_tab_match(Queries.get_fixtures(2014,2,4)))  # La Liga
        sub_stack.addWidget(UILoader.create_sub_tab_match(Queries.get_fixtures(2002,2,4)))  # Bundesliga
        sub_stack.addWidget(UILoader.create_sub_tab_match(Queries.get_fixtures(2019,2,4)))  # Serie A
        sub_stack.addWidget(UILoader.create_sub_tab_match(Queries.get_fixtures(2015,2,4)))  # Ligue 1

        section_layout.addWidget(sub_stack)

        # Create a scroll area to wrap the section widget
        scroll_area = qtw.QScrollArea()
        scroll_area.setWidgetResizable(True)  
        scroll_area.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAsNeeded)  
        scroll_area.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)  
        scroll_area.setWidget(section_widget)
        section_widget.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Expanding)
        section_widget.setMinimumWidth(scroll_area.viewport().width())  
        
        main_layout.addWidget(scroll_area)

        # Subtab buttons
        sub_tab_bar_layout = qtw.QHBoxLayout()
        buttons = ["Main", "Subscribed", "UCL", "EPL", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]
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

        # Create a stacked widget to hold the different league sub-tabs
        league_stack = qtw.QStackedWidget(main_window)

        # Add another sub-stacked widget for standings, stats, and fixtures
        def create_secondary_stack(competition_id):
            secondary_stack = qtw.QStackedWidget(main_window)

            # Create sub-tabs for standings, stats, and fixtures
            standings_tab = UILoader.create_sub_tab_stats(Queries.get_competition_standings(competition_id),0)
            teams_tab =UILoader.create_sub_tab_stats(Queries.get_competition_stats(competition_id),1)
            players_tab = UILoader.create_sub_tab_stats(Queries.get_player_stats(competition_id),2) 
            fixtures_tab = UILoader.create_sub_tab_stats(Queries.get_fixtures(competition_id),3)

            secondary_stack.addWidget(standings_tab)  # Standings
            secondary_stack.addWidget(teams_tab)      # Teams
            secondary_stack.addWidget(players_tab)    # Players
            secondary_stack.addWidget(fixtures_tab)   # Fixtures

            return secondary_stack

        # Add secondary stacks for each league
        league_stack.addWidget(create_secondary_stack(2001))  # UCL
        league_stack.addWidget(create_secondary_stack(2021))  # EPL
        league_stack.addWidget(create_secondary_stack(2014))  # La Liga
        league_stack.addWidget(create_secondary_stack(2002))  # Bundesliga
        league_stack.addWidget(create_secondary_stack(2019))  # Serie A
        league_stack.addWidget(create_secondary_stack(2015))  # Ligue 1

        section_layout.addWidget(league_stack)
        
        scroll_area = qtw.QScrollArea()
        scroll_area.setWidgetResizable(True)  
        scroll_area.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAsNeeded)  
        scroll_area.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)  
        scroll_area.setWidget(section_widget)
        section_widget.setSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Expanding)
        section_widget.setMinimumWidth(scroll_area.viewport().width())  
        
        main_layout.addWidget(scroll_area)


        sub_index=0
        
        # League subtab buttons
        league_tab_bar_layout = qtw.QHBoxLayout()
        leagues = ["UCL", "EPL", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]
        for i, name in enumerate(leagues):
            btn = qtw.QPushButton(name)
            btn.setStyleSheet("QPushButton { text-align: center; }")
            btn.clicked.connect(lambda _, idx=i: UILoader.update_sub_tab_buttons(league_tab_bar_layout, idx, btn, league_stack))
            btn.clicked.connect(lambda _, idx=i: UILoader.update_sub_tab_buttons(secondary_tab_bar_layout, sub_index, secondary_tab_bar_layout.itemAt(1).widget(), league_stack.currentWidget()))
            league_tab_bar_layout.addWidget(btn)

        # Add league tab buttons at the top
        main_layout.insertLayout(0, league_tab_bar_layout)

        # Subtab buttons for standings, stats, and fixtures
        secondary_tab_bar_layout = qtw.QHBoxLayout()
        sub_tabs = ["Standings", "Teams", "Players", "Fixtures"]
        for i, name in enumerate(sub_tabs):
            btn = qtw.QPushButton(name)
            btn.setStyleSheet("QPushButton { text-align: center; }")
            btn.clicked.connect(lambda _, idx=i: UILoader.update_sub_tab_buttons(secondary_tab_bar_layout, idx, btn, league_stack.currentWidget(),0))
            secondary_tab_bar_layout.addWidget(btn)

        # Insert the secondary sub-tab buttons below the league buttons
        main_layout.insertLayout(1, secondary_tab_bar_layout)
        
        # Set default selection for both tabs
        UILoader.update_sub_tab_buttons(league_tab_bar_layout, 0, league_tab_bar_layout.itemAt(0).widget(), league_stack)
        UILoader.update_sub_tab_buttons(secondary_tab_bar_layout, 0, secondary_tab_bar_layout.itemAt(1).widget(), league_stack.currentWidget())  

        stats_tab.setLayout(main_layout)

        return stats_tab


    # Function to create content for each sub-tab with stats data
    @staticmethod
    def create_sub_tab_stats(stats, idx):
        widget = qtw.QWidget()
        layout = qtw.QVBoxLayout()

        if stats:
            # Create headers
            Stats.create_headers(layout, idx)
            layout.addSpacing(10)

            if idx == 2:  # Player stats
                for category, player_stats in stats.items():
                    if player_stats:
                        category_label = qtw.QLabel(f"{category.replace('_', ' ').title()}")
                        category_label.setStyleSheet("font-weight: bold; font-size: 14px;")
                        layout.addWidget(category_label)

                        for player_stat in player_stats:
                            if category == "top_scorers":
                                stat_label = f"{player_stat['player_name']}    Goals: {player_stat['total_goals']}"
                            elif category == "top_assist_providers":
                                stat_label = f"{player_stat['player_name']}    Assists: {player_stat['total_assists']}"
                            elif category == "top_yellow_card_recipients":
                                stat_label = f"{player_stat['player_name']}    Yellow Cards: {player_stat['total_yellow_cards']}"
                            elif category == "top_red_card_recipients":
                                stat_label = f"{player_stat['player_name']}    Red Cards: {player_stat['total_red_cards']}"
                            elif category == "top_clean_sheet_providers":
                                stat_label = f"{player_stat['player_name']}    Clean Sheets: {player_stat['total_clean_sheets']}"
                        
                            layout.addWidget(qtw.QLabel(stat_label))
                        layout.addSpacing(10)
                    else:
                        no_stat_label = qtw.QLabel(f"No stats available for {category.replace('_', ' ').title()}")
                        layout.addWidget(no_stat_label)

            else: 
                if isinstance(stats, list):  # Team stats should be a list of dicts
                    team_rank = 1
                    for stat in stats:
                        if isinstance(stat, dict):
                            Stats.create_team_row(layout, team_rank, stat, idx)
                            team_rank += 1
                        else:
                            print(f"Unexpected stat format: {stat}")
                            stat_label = qtw.QLabel("Invalid stat format")
                            layout.addWidget(stat_label)
                else:
                    print(f"Unexpected stat structure for team stats: {stats}")
        else:
            no_stat_label = qtw.QLabel("No stats available")
            layout.addWidget(no_stat_label)

        layout.addStretch()
        widget.setLayout(layout)
        return widget


    
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
        news_layout = Favorite.create_news_layout(favorite_team)
        
        # Create the Fixture and Stats tabs
        fixture_tab = qtw.QWidget()
        fixture_tab.setLayout(fixture_layout)

        stats_tab = qtw.QWidget()
        stats_tab.setLayout(stats_layout)

        news_tab = qtw.QWidget()
        news_tab.setLayout(news_layout)
    
        # Add the fixture and stats tabs to the stacked widget
        sub_stack.addWidget(fixture_tab)  
        sub_stack.addWidget(stats_tab) 
        sub_stack.addWidget(news_tab) 

        section_layout.addWidget(sub_stack)
        main_layout.addWidget(section_widget)

        # Subtab buttons
        sub_tab_bar_layout = qtw.QHBoxLayout()
        buttons = ["Fixture", "Stats","News"]
        for i, name in enumerate(buttons):
            btn = qtw.QPushButton(name)
            btn.setStyleSheet("QPushButton { text-align: center; }")
            btn.clicked.connect(lambda _, idx=i: (
                sub_stack.setCurrentIndex(idx),
                UILoader.update_sub_tab_buttons(sub_tab_bar_layout, idx, btn, sub_stack)
            ))
            sub_tab_bar_layout.addWidget(btn)

        main_layout.insertLayout(0, sub_tab_bar_layout)

        UILoader.update_sub_tab_buttons(sub_tab_bar_layout, 0, sub_tab_bar_layout.itemAt(0).widget(), sub_stack)

        favorite_tab.setLayout(main_layout)

        return favorite_tab

    @staticmethod
    def update_sub_tab_buttons(layout, active_index, active_button, sub_stack, should=1):
        for i in range(layout.count()):
            button = layout.itemAt(i).widget()
            if should==0:
                sub_index=active_index
            if i == active_index: 
                button.setStyleSheet("QPushButton { text-align: center; font-weight: bold; }")
            else:
                button.setStyleSheet("QPushButton { text-align: center; }")
        sub_stack.setCurrentIndex(active_index)


    


   

    
       
