import json
import os
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QByteArray
from Queries import Queries
from News import News

FAVORITE_TEAM_FILE = "favorite_team.json"

class Favorite:
    column_widths = {
        "Team": 200,
        "P": 50, 
        "W": 50, 
        "D": 50, 
        "L": 50, 
        "F/A": 50,
        "Pts": 50
    }
    @staticmethod
    def create_headers(layout):
        header_layout = qtw.QGridLayout()
        headers = ["Team", "P", "W", "D", "L", "F/A", "Pts"]

        for idx, header in enumerate(headers):
            label = qtw.QLabel(header)
            label.setFixedWidth(Favorite.column_widths.get(header, 50))
            header_layout.addWidget(label, 0, idx, alignment=qtc.Qt.AlignCenter)

        layout.addLayout(header_layout)
        
    @staticmethod
    def get_favorite_team():
        if os.path.exists(FAVORITE_TEAM_FILE):
            with open(FAVORITE_TEAM_FILE, 'r') as f:
                data = json.load(f)
                short_name = data.get("short_name", None)
                team_id = data.get("team_id", None)
                print(f"Favorite team found:  (ID: {team_id})")
                Queries.set_fav_team_matches_as_subscribed(team_id)
                return short_name, team_id  
        return None, None

    @staticmethod
    def set_favorite_team(full_name,mainwindow):
        # Get team ID from the database
        team_id = Queries.get_team_id_by_name(full_name)
        from UILoader import UILoader
        if team_id:
            with open(FAVORITE_TEAM_FILE, 'w') as f:
                json.dump({"short_name": full_name, "team_id": team_id}, f)
                print(f"Favorite team set: {full_name} (ID: {team_id})")
                Queries.set_fav_team_matches_as_subscribed(team_id)
        else:
            print(f"Team {full_name} not found in the database.")

    @staticmethod
    def prompt_set_favorite_team(main_window):
        dialog = qtw.QDialog(main_window) 
        dialog.setWindowTitle("Set Favorite Team")
    
        dialog.setWindowFlags(dialog.windowFlags() & ~qtc.Qt.WindowContextHelpButtonHint)
        dialog.setGeometry(main_window.x(), main_window.y()+30, 725, 1010)
        dialog.setLayout(qtw.QVBoxLayout())

        label = qtw.QLabel("Please start typing your favorite team:")
        dialog.layout().addWidget(label)

        teams = Queries.fetch_teams_from_database()  
    
        team_input = qtw.QLineEdit()
        completer = qtw.QCompleter(teams)  
        completer.setCaseSensitivity(qtc.Qt.CaseInsensitive) 
        completer.setFilterMode(qtc.Qt.MatchContains)  
        completer.setCompletionMode(qtw.QCompleter.UnfilteredPopupCompletion)
        team_input.setCompleter(completer)
        dialog.layout().addWidget(team_input)

        # Ok button
        ok_button = qtw.QPushButton("OK")
        ok_button.clicked.connect(lambda: Favorite.set_favorite_team(team_input.text(),main_window) or dialog.accept())
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

        fixture_layout = qtw.QVBoxLayout()

        # Add favorite team information
        if favorite_team:
            fixture_layout.addWidget(qtw.QLabel(f"<b>Favorite Team: {favorite_team}</b>"))

            # Display last 2 matches
            fixture_layout.addWidget(qtw.QLabel("<b>Previous Matches:</b>"))
            if last_matches:
                for match in last_matches:
                    fixture_layout.addWidget(qtw.QLabel(
                        f"{match['competition']} R{match['matchday']}: "
                        f"{match['team1']} {match['score1']} - {match['score2']} {match['team2']} on {match['date']}"))
            else:
                fixture_layout.addWidget(qtw.QLabel("No recent matches available"))

            # Display next 2 matches
            fixture_layout.addWidget(qtw.QLabel("<b>Next Matches:</b>"))
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

        stats_layout = qtw.QVBoxLayout()

        if favorite_team_id:
            team_stats = Queries.get_team_stats_in_fav(favorite_team_id)

            # Add team statistics
            stats_layout.addWidget(qtw.QLabel(f"Team Stats for {favorite_team}:"))          
            if team_stats:
                for index, stat in enumerate(team_stats):
                    stats_layout.addWidget(qtw.QLabel(f"Competition: {stat['competition']}"))
                    Favorite.create_sub_tab_stats(stats_layout, Queries.get_competition_standings_near_team(stat['competition_id'], favorite_team_id))                   
                    stats_layout.addWidget(qtw.QLabel(f"Goals Scored: {stat['goals_scored']}"))
                    stats_layout.addWidget(qtw.QLabel(f"Goals Conceded: {stat['goals_conceded']}"))
                    stats_layout.addWidget(qtw.QLabel(f"Goal Difference: {stat['goal_difference']}"))

                    if stat['biggest_win']:
                        biggest_win = stat['biggest_win']
                        
                        win_text = f"Biggest Win: {biggest_win['team_goals']} - {biggest_win['opponent_goals']} " \
                                   f"against {biggest_win['opponent']} on {biggest_win['date']} R{biggest_win['matchday']}"
                        stats_layout.addWidget(qtw.QLabel(win_text))
                    else:
                        stats_layout.addWidget(qtw.QLabel("No biggest wins available."))
                        
                    if stat['biggest_loss']:
                        biggest_loss = stat['biggest_loss']
                        loss_text = f"Biggest Loss: {biggest_loss['team_goals']} - {biggest_loss['opponent_goals']} " \
                                    f"against {biggest_loss['opponent']} on {biggest_loss['date']} R{biggest_loss['matchday']}"
                        stats_layout.addWidget(qtw.QLabel(loss_text))
                    else:
                        stats_layout.addWidget(qtw.QLabel("No biggest loss available."))

                        
                    if index < len(team_stats) - 1:
                        stats_layout.addWidget(qtw.QLabel("-" * 70))
            else:
                stats_layout.addWidget(qtw.QLabel("No stats available for this team."))
        else:
            stats_layout.addWidget(qtw.QLabel("No favorite team set for stats."))

        stats_layout.addStretch()
        return stats_layout
    
    @staticmethod
    def create_news_layout(favorite_team_id):
        news_layout = qtw.QVBoxLayout()
        stacked_widget = qtw.QStackedWidget()

        news_scroll_area = qtw.QScrollArea()
        news_scroll_area.setWidgetResizable(True)

        news_content_widget = qtw.QWidget()
        news_content_layout = qtw.QVBoxLayout(news_content_widget)
        news_data = News.get_fav_team_news_headlines(favorite_team_id)
    
        if favorite_team_id == -1:
            news_data = News.show_news_in_home()
        
        for news_item in news_data:
            news_headline = news_item.get("title", "No Title")
            news_link = news_item.get("link", "#")

            headline_label = qtw.QLabel(f"<a href='#'>{news_headline}</a>")
            headline_label.setTextFormat(qtc.Qt.RichText)
            headline_label.setTextInteractionFlags(qtc.Qt.TextBrowserInteraction)
            headline_label.setOpenExternalLinks(False)  
            font = headline_label.font()
            font.setPointSize(12)  
            headline_label.setFont(font)
            headline_label.linkActivated.connect(lambda _, link=news_link: display_article_content(link))

            news_content_layout.addWidget(headline_label)

        news_content_widget.setLayout(news_content_layout)
        news_scroll_area.setWidget(news_content_widget)

        article_widget = qtw.QWidget()
        article_layout = qtw.QVBoxLayout(article_widget)

        back_button = qtw.QPushButton("Back to News")
        back_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(0))
        article_layout.addWidget(back_button)

        article_scroll_area = qtw.QScrollArea()
        article_scroll_area.setWidgetResizable(True)

        article_content_widget = qtw.QWidget()
        article_content_layout = qtw.QVBoxLayout(article_content_widget)

        image_label = qtw.QLabel()
        image_label.setAlignment(qtc.Qt.AlignCenter)

        article_content_label = qtw.QTextBrowser()

        article_content_layout.addWidget(image_label)
        article_content_layout.addWidget(article_content_label)

        article_content_widget.setLayout(article_content_layout)

        article_scroll_area.setWidget(article_content_widget)

        article_layout.addWidget(article_scroll_area)

        stacked_widget.addWidget(news_scroll_area)
        stacked_widget.addWidget(article_widget)

        def display_article_content(link):
            paragraphs, img_url = News.scrape_news_paragraphs(link)

            if paragraphs:
                article_content_label.setText(paragraphs)
                font = article_content_label.font()
                font.setPointSize(10)
                article_content_label.setFont(font)
            else:
                article_content_label.setText("No content available.")

            if img_url != "No image found":
                image_data = requests.get(img_url).content
                pixmap = QPixmap()
                pixmap.loadFromData(QByteArray(image_data))
                pixmap = pixmap.scaled(400, 400, aspectRatioMode=qtc.Qt.KeepAspectRatio)
                image_label.setPixmap(pixmap)
                image_label.show()  
            else:
                image_label.clear()  

            stacked_widget.setCurrentIndex(1)

        news_layout.addWidget(stacked_widget)

        return news_layout



    @staticmethod
    def create_team_row(layout, stat):
        team_layout = qtw.QGridLayout()

        team_label = qtw.QLabel(f"{stat['team_pos']}. {stat['team_name']}")
        team_label.setMinimumWidth(Favorite.column_widths["Team"])
        team_layout.addWidget(team_label, 0, 0, alignment=qtc.Qt.AlignLeft)
        stats = [
            f"{stat['wins'] + stat['losses'] + stat['draws']}",  
            f"{stat['wins']}",  
            f"{stat['draws']}",  
            f"{stat['losses']}",  
            f"{stat['goals_scored']} / {stat['goals_conceded']}",  
            f"{stat['points']}"  
        ]

        for n, stat_value in enumerate(stats, start=1):
            stat_label = qtw.QLabel(stat_value)
            stat_label.setFixedWidth(Favorite.column_widths[list(Favorite.column_widths.keys())[n]])
            team_layout.addWidget(stat_label, 0, n, alignment=qtc.Qt.AlignCenter)
            
        blank_label = qtw.QLabel(" ")
        team_layout.addWidget(blank_label, 1, 0, 1, len(stats) + 1)
        layout.addLayout(team_layout)

    @staticmethod
    def create_sub_tab_stats(layout, stats):

        Favorite.create_headers(layout)
        layout.addSpacing(10)
        if stats:

            if isinstance(stats, list):  
                for stat in stats:
                    if isinstance(stat, dict):
                        Favorite.create_team_row(layout, stat)
                    else:
                        print(f"Unexpected stat format: {stat}")
                        stat_label = qtw.QLabel("Invalid stat format")
                        layout.addWidget(stat_label)
            else:
                print(f"Unexpected stat structure for team stats: {stats}")
        else:
            no_stat_label = qtw.QLabel("No stats available")
            layout.addWidget(no_stat_label)

        