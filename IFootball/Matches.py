from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc, QtGui as qtg
import os
from Queries import Queries

class Matches:
    column_widths = {
        "Date": 150,
        "Matchday": 120,
        "Home": 150,
        "Score": 100,
        "Away": 150,
        "": 70
    }
    image_cache = {}

    @staticmethod
    def create_headers(layout):
        header_layout = qtw.QGridLayout()
        headers = ["Date", "Matchday", "Home", "Score", "Away", ""]
        header_layout.setContentsMargins(30, 0, 0, 0)

        for idx, header in enumerate(headers):
            label = qtw.QLabel(header)
            label.setFixedWidth(Matches.column_widths.get(header, 50))

            if header in ["Home", "Score"]:
                label.setContentsMargins(30, 0, 0, 0) 
            elif header in "Away":
                label.setContentsMargins(55, 0, 0, 0) 

            header_layout.addWidget(label, 0, idx, alignment=qtc.Qt.AlignCenter)

        layout.addLayout(header_layout)

    @staticmethod
    def create_match_row(layout, match):
        match_layout = qtw.QGridLayout()

        date_label = qtw.QLabel(match['match_date'].strftime('%Y-%m-%d %H:%M'))
        date_label.setMinimumWidth(Matches.column_widths["Date"])
        match_layout.addWidget(date_label, 0, 0, alignment=qtc.Qt.AlignLeft)

        round_label = qtw.QLabel(f"{match['matchday']}")
        round_label.setMinimumWidth(Matches.column_widths["Matchday"])
        match_layout.addWidget(round_label, 0, 1, alignment=qtc.Qt.AlignLeft)

        home_team_layout = qtw.QHBoxLayout()
        home_team_layout.addWidget(Matches.get_team_crest(match['home_team_id']))
        home_team_label = qtw.QLabel(f"{match['home_team']}")
        home_team_label.setMinimumWidth(Matches.column_widths["Home"])
        home_team_layout.addWidget(home_team_label)
        match_layout.addLayout(home_team_layout, 0, 2, alignment=qtc.Qt.AlignLeft)

        home_score = match['home_score']
        away_score = match['away_score']
        score_display = (
            f"{home_score} : {away_score}"
            if home_score is not None and away_score is not None and home_score >= 0 and away_score >= 0
            else "  vs"
        )
        score_label = qtw.QLabel(score_display)
        score_label.setMinimumWidth(Matches.column_widths["Score"])
        score_label.setContentsMargins(15, 0, 0, 0)
        match_layout.addWidget(score_label, 0, 3, alignment=qtc.Qt.AlignCenter)

        away_team_layout = qtw.QHBoxLayout()
        away_team_layout.setContentsMargins(0, 0, 15, 0) 
        away_team_layout.addWidget(Matches.get_team_crest(match['away_team_id']))
        away_team_label = qtw.QLabel(match['away_team'])
        away_team_label.setMinimumWidth(Matches.column_widths["Away"])
        away_team_layout.addWidget(away_team_label)
        match_layout.addLayout(away_team_layout, 0, 4, alignment=qtc.Qt.AlignLeft)

        bookmark_label = qtw.QLabel()
        Matches.set_bookmark_image(bookmark_label, match.get('subscribed'))
        bookmark_label.mousePressEvent = lambda event: Matches.toggle_bookmark(bookmark_label, match)
        match_layout.addWidget(bookmark_label, 0, 5, alignment=qtc.Qt.AlignCenter)

        layout.addLayout(match_layout)


        
    @staticmethod
    def get_bookmark_image(subscribed):
        image_name = "subscribed.png" if subscribed == 'Yes' else "notSubscribed.png"
  
        if image_name not in Matches.image_cache:
            image_path = os.path.join(os.path.dirname(__file__), 'images', image_name)
            pixmap = qtg.QPixmap(image_path).scaled(30, 30, qtc.Qt.KeepAspectRatio)
            Matches.image_cache[image_name] = pixmap

        return Matches.image_cache[image_name]

    @staticmethod
    def set_bookmark_image(label, subscribed):
        pixmap = Matches.get_bookmark_image(subscribed)
        label.setPixmap(pixmap)

    @staticmethod
    def toggle_bookmark(label, match):
        new_status = 'No' if match.get('subscribed') == 'Yes' else 'Yes'
        match['subscribed'] = new_status  
        Queries.toggle_match_as_subscribed(match['match_id'],new_status)  
        Matches.set_bookmark_image(label, new_status)
        from UILoader import UILoader
        UILoader.should_reload_for_subscribed = True

    @staticmethod
    def get_team_crest(team_id,main = 0):
        crests_dir = os.path.join(os.path.dirname(__file__), 'crests')
        crest_path = os.path.join(crests_dir, f"{team_id}.png")

        if os.path.exists(crest_path):
            pixmap = qtg.QPixmap(crest_path).scaled(30, 30, qtc.Qt.KeepAspectRatio)
        else:
            pixmap = qtg.QPixmap(30, 30)
            pixmap.fill(qtg.QColor("gray"))
        if main == 1:
            return pixmap
        label = qtw.QLabel()
        label.setPixmap(pixmap)
        return label

    @staticmethod
    def setup_match_display(match_data):
        app = qtw.QApplication([])
        window = qtw.QWidget()
        window.setWindowTitle("Match Statistics")

        main_layout = qtw.QVBoxLayout()

        Matches.create_headers(main_layout)

        for match in match_data:
            Matches.create_match_row(main_layout, match)

        window.setLayout(main_layout)
        window.show()
        app.exec_()
