from Queries import Queries
import PyQt5.QtWidgets as qtw
import PyQt5.QtCore as qtc

class Stats:
    column_widths = {
        "Team": 200,  # Width for team names
        "P": 50, 
        "W": 50, 
        "D": 50, 
        "L": 50, 
        "F/A": 50, 
        "Pts": 50,
        "GF": 50, 
        "GA": 50, 
        "YC": 50, 
        "RC": 50, 
        "Shots": 50,
        "On Target": 50,
        "Offsides": 60,
        "Fouls": 50,
        "Date": 150, 
        "Matchday": 50,
        "Home":100,
        "Away":100,
        "": 50
    }

    @staticmethod
    def create_headers(layout, idx):
        header_layout = qtw.QGridLayout()

        if idx == 0:  
            headers = ["Team", "P", "W", "D", "L", "F/A", "Pts"]
        elif idx == 1:  
            headers = ["Team", "P", "GF", "GA", "YC", "RC", "Shots", "On Target", "Offsides", "Fouls"]
        elif idx == 2:  
            headers = []
        elif idx == 3:
            headers = ["Date", "Matchday", "Home", "", "Away"]

        for idx, header in enumerate(headers):
            label = qtw.QLabel(header)
            label.setFixedWidth(Stats.column_widths[header])
            header_layout.addWidget(label, 0, idx, alignment=qtc.Qt.AlignCenter)
        # Add header layout to main layout
        layout.addLayout(header_layout)

    @staticmethod
    def create_team_row(layout, team_rank, stat, idx):
        team_layout = qtw.QGridLayout()

        if idx == 0:
            team_label = qtw.QLabel(f"{team_rank}. {stat['team_name']}")
            team_label.setMinimumWidth(Stats.column_widths["Team"])
            team_layout.addWidget(team_label, 0, 0, alignment=qtc.Qt.AlignLeft)
            stats = [
                f"{stat['wins'] + stat['losses'] + stat['draws']}",  
                f"{stat['wins']}",  
                f"{stat['draws']}",  
                f"{stat['losses']}",  
                f"{stat['goals_scored']} / {stat['goals_conceded']}",  
                f"{stat['points']}"  
            ]
        elif idx == 1:
            team_label = qtw.QLabel(f"{stat['team_name']}")
            team_label.setMinimumWidth(Stats.column_widths["Team"])
            team_layout.addWidget(team_label, 0, 0, alignment=qtc.Qt.AlignLeft)
            stats = [
                f"{stat['matches_played']}",
                f"{stat['goals_scored']}",  
                f"{stat['goals_conceded']}", 
                f"{stat['yellow_cards']}",  
                f"{stat['red_cards']}",
                f"{stat['total_shots']}",
                f"{stat['on_target']}",
                f"{stat['offsides']}",
                f"{stat['fouls']}"
            ]
        elif idx == 3: 
            date_label = qtw.QLabel(f"{stat['match_date']}")
            date_label.setMinimumWidth(Stats.column_widths["Date"])
            team_layout.addWidget(date_label, 0, 0, alignment=qtc.Qt.AlignLeft)
            
            round_label = qtw.QLabel(f"{stat['matchday']}")
            round_label.setMinimumWidth(Stats.column_widths["Matchday"])
            team_layout.addWidget(round_label, 0, 1, alignment=qtc.Qt.AlignCenter)

            home_team_label = qtw.QLabel(f"{stat['home_team']}")
            home_team_label.setMinimumWidth(Stats.column_widths["Home"])
            team_layout.addWidget(home_team_label, 0, 2, alignment=qtc.Qt.AlignLeft)

            home_score = stat['home_score']
            away_score = stat['away_score']
        
            # Check if home_score or away_score is invalid
            if home_score is None or away_score is None or home_score < 0 or away_score < 0:
                score_display = "  vs"
            else:
                score_display = f"{home_score} : {away_score}"
        
            score_label = qtw.QLabel(score_display)
            score_label.setMinimumWidth(Stats.column_widths[""])
            team_layout.addWidget(score_label, 0, 3, alignment=qtc.Qt.AlignCenter)

            away_team_label = qtw.QLabel(f"{stat['away_team']}")
            away_team_label.setMinimumWidth(Stats.column_widths["Away"])
            team_layout.addWidget(away_team_label, 0, 4, alignment=qtc.Qt.AlignLeft)

        # Apply the stats
        if idx<3: 
            for n, stat_value in enumerate(stats, start=1):
                stat_label = qtw.QLabel(stat_value)
                stat_label.setFixedWidth(Stats.column_widths[list(Stats.column_widths.keys())[n]])
                team_layout.addWidget(stat_label, 0, n, alignment=qtc.Qt.AlignCenter)

        layout.addLayout(team_layout)
