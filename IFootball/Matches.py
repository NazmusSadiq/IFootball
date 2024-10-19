from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc , QtGui as qtg
import os

class Matches:
    column_widths = {
        "Date": 150,
        "Matchday": 100,
        "Home": 150,
        "Score": 100,
        "Away": 150,
        "": 50
    }
    @staticmethod
    def create_headers(layout):
        header_layout = qtw.QGridLayout()
        headers = ["Date", "Matchday", "Home", "Score", "Away"]

        for idx, header in enumerate(headers):
            label = qtw.QLabel(header)
            label.setFixedWidth(Matches.column_widths[header])
            header_layout.addWidget(label, 0, idx, alignment=qtc.Qt.AlignCenter)

        layout.addLayout(header_layout)

    @staticmethod
    def create_match_row(layout, match):
        match_layout = qtw.QGridLayout()

        # Date Label
        date_label = qtw.QLabel(f"{match['match_date']}")
        date_label.setMinimumWidth(Matches.column_widths["Date"])
        match_layout.addWidget(date_label, 0, 0, alignment=qtc.Qt.AlignLeft)

        # Matchday Label
        round_label = qtw.QLabel(f"{match['matchday']}")
        round_label.setMinimumWidth(Matches.column_widths["Matchday"])
        match_layout.addWidget(round_label, 0, 1, alignment=qtc.Qt.AlignCenter)

        # Home Team Name and Crest
        home_team_layout = qtw.QHBoxLayout()
        home_team_layout.addWidget(Matches.get_team_crest(match['home_team_id']))
        home_team_label = qtw.QLabel(f"{match['home_team']}")
        home_team_label.setMinimumWidth(Matches.column_widths["Home"])
        home_team_layout.addWidget(home_team_label)
        match_layout.addLayout(home_team_layout, 0, 2)

        # Score Label
        home_score = match['home_score']
        away_score = match['away_score']
        
        current_match_id = match['match_id']
         # Displaying score or 'vs' if scores are invalid
        if home_score is None or away_score is None or home_score < 0 or away_score < 0:
            score_display = "  vs"
        else:
            score_display = f"{home_score} : {away_score}"
        score_label = qtw.QLabel(score_display)
        score_label.setMinimumWidth(Matches.column_widths[""])
        match_layout.addWidget(score_label, 0, 3, alignment=qtc.Qt.AlignCenter)

        # Away Team Crest and Name
        away_team_layout = qtw.QHBoxLayout()
        away_team_label = qtw.QLabel(match['away_team'])
        away_team_label.setMinimumWidth(Matches.column_widths["Away"])
        away_team_layout.addWidget(away_team_label)
        away_team_layout.addWidget(Matches.get_team_crest(match['away_team_id']))
        match_layout.addLayout(away_team_layout, 0, 4)
        # print(match)
        # Add the match layout to the main layout
        layout.addLayout(match_layout)

    @staticmethod
    def get_team_crest(team_id):
        """Returns a QLabel with the team crest image."""
        crests_dir = os.path.join(os.path.dirname(__file__), 'crests')
        crest_path = os.path.join(crests_dir, f"{team_id}.png")

        # Load the image if it exists, else show a placeholder
        if os.path.exists(crest_path):
            pixmap = qtg.QPixmap(crest_path).scaled(30, 30, qtc.Qt.KeepAspectRatio)
        else:
            print(crest_path)
            pixmap = qtg.QPixmap(30, 30)  # Create an empty pixmap as a placeholder
            pixmap.fill(qtg.QColor("gray"))

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

# Sample data for testing
if __name__ == "__main__":
    sample_matches = [
        {"match_date": "2024-10-01", "round": "1", "home_team": "Team A", "home_score": 2, "away_team": "Team B", "away_score": 1},
        {"match_date": "2024-10-02", "round": "2", "home_team": "Team C", "home_score": 0, "away_team": "Team D", "away_score": 3},
        {"match_date": "2024-10-03", "round": "3", "home_team": "Team E", "home_score": None, "away_team": "Team F", "away_score": None},
    ]

    Matches.setup_match_display(sample_matches)
