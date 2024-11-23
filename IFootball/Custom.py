import json
from PyQt5.sip import delete
import requests
from CustomQueries import CustomQueries
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox

class Custom:
    column_widths = {
        "Matchday": 120,
        "Home": 150,
        "Score": 100,
        "Away": 150,
        "": 70
    }
    selected_comp_id= None

    @staticmethod
    def create_headers(layout):
        header_layout = qtw.QGridLayout()
        headers = ["Matchday","Home", "Score", "Away", ""]
        header_layout.setContentsMargins(35, 0, 0, 0)

        for idx, header in enumerate(headers):
            label = qtw.QLabel(header)
            label.setFixedWidth(Custom.column_widths.get(header, 50))
            if header in ["Score"]:
                label.setContentsMargins(35, 0, 0, 0)
            if header in ["Away"]:
                label.setContentsMargins(55, 0, 0, 0)
            header_layout.addWidget(label, 0, idx, alignment=qtc.Qt.AlignCenter)

        layout.addLayout(header_layout)

    @staticmethod
    def create_custom_match_row(layout, match):
        match_layout = qtw.QGridLayout()
        
        round_label = qtw.QLabel(f"{match['matchday']}")
        round_label.setMinimumWidth(Custom.column_widths["Matchday"])
        round_label.setContentsMargins(50, 0, 0, 0)
        match_layout.addWidget(round_label, 0, 0, alignment=qtc.Qt.AlignLeft)
        
        home_team_layout = qtw.QHBoxLayout()
        home_team_layout.addWidget(CustomQueries.get_team_crest(match['home_team_id']))
        home_team_label = qtw.QLabel(f"{match['home_team']}")
        home_team_label.setMinimumWidth(Custom.column_widths["Home"])
        home_team_layout.addWidget(home_team_label)
        home_team_layout.setContentsMargins(20, 0, 0, 0)
        match_layout.addLayout(home_team_layout, 0, 1)

        home_score = match['home_score']
        away_score = match['away_score']
        score_display = (
            f"{home_score} : {away_score}"
            if home_score is not None and away_score is not None and home_score >= 0 and away_score >= 0
            else "  vs"
        )
        score_label = qtw.QLabel(score_display)
        score_label.setMinimumWidth(Custom.column_widths["Score"])
        match_layout.addWidget(score_label, 0, 2, alignment=qtc.Qt.AlignCenter)

        away_team_layout = qtw.QHBoxLayout()
        away_team_label = qtw.QLabel(match['away_team'])
        away_team_layout.addWidget(CustomQueries.get_team_crest(match['away_team_id']))
        away_team_label.setMinimumWidth(Custom.column_widths["Away"])
        away_team_layout.addWidget(away_team_label)
        match_layout.addLayout(away_team_layout, 0, 3)

        layout.addLayout(match_layout)
    
    @staticmethod
    def get_competition_input(main_window):
        dialog = qtw.QDialog(main_window)
        dialog.setWindowTitle("Add Competition")
        dialog.resize(main_window.size())
        
        layout = qtw.QVBoxLayout()

        name_label = qtw.QLabel("Enter Competition Name:")
        layout.addWidget(name_label)
        name_input = qtw.QLineEdit()
        layout.addWidget(name_input)

        code_label = qtw.QLabel("Enter Competition Code:")
        layout.addWidget(code_label)
        code_input = qtw.QLineEdit()
        layout.addWidget(code_input)

        num_teams_label = qtw.QLabel("Enter the Number of Teams for the Competition:")
        layout.addWidget(num_teams_label)
        num_teams_input = qtw.QSpinBox()
        num_teams_input.setMinimum(2)
        num_teams_input.setMaximum(20)
        
        def enforce_even_number(value):
            if value % 2 != 0:
                num_teams_input.setValue(value + 1 if value < 20 else value - 1)

        num_teams_input.valueChanged.connect(enforce_even_number)
        layout.addWidget(num_teams_input)

        crest_label = qtw.QLabel("Select Competition Crest:")
        layout.addWidget(crest_label)
        crest_button = qtw.QPushButton("Choose Crest")
        crest_path_label = qtw.QLabel("(No crest selected)")
        crest_file = None  

        def select_crest():
            nonlocal crest_file
            file, _ = QFileDialog.getOpenFileName(main_window, "Select Competition Crest", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
            if file:
                crest_file = file
                crest_path_label.setText(file)

        crest_button.clicked.connect(select_crest)
        layout.addWidget(crest_button)
        layout.addWidget(crest_path_label)

        button_box = qtw.QDialogButtonBox(qtw.QDialogButtonBox.Ok | qtw.QDialogButtonBox.Cancel)
        layout.addWidget(button_box)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        dialog.setLayout(layout)

        if dialog.exec_() == qtw.QDialog.Accepted:
            competition_name = name_input.text().strip()
            competition_code = code_input.text().strip()
            num_teams = num_teams_input.value()

            return competition_name, competition_code, crest_file, num_teams

        return None, None, None, None


    @staticmethod
    def create_fixtures_layout():
        fixtures_layout = qtw.QVBoxLayout()
        Custom.create_sub_tab_match(fixtures_layout)
        fixtures_layout.addStretch()
        return fixtures_layout

    @staticmethod
    def create_stats_layout():
        from Favorite import Favorite
        stats_layout = qtw.QVBoxLayout()  
        Favorite.create_sub_tab_stats(stats_layout, CustomQueries.get_competition_standings(Custom.selected_comp_id))                   
        stats_layout.addStretch()
        return stats_layout

        
    @staticmethod
    def add_new_competition(main_window, main_layout):
        competition_name, competition_code, competition_crest, num_teams = Custom.get_competition_input(main_window)

        if not competition_name or not competition_code:
            QMessageBox.warning(main_window, "Invalid Input", "Competition name, code, and number of teams cannot be empty.")
            return

        if num_teams <= 0:
            QMessageBox.warning(main_window, "Invalid Input", "Number of teams must be greater than 0.")
            return

        # Create a dialog to collect team names and crests
        teams_layout = qtw.QVBoxLayout()
        team_data = []  

        for i in range(num_teams):
            team_layout = qtw.QHBoxLayout()
            team_name_input = qtw.QLineEdit()
            team_name_input.setPlaceholderText(f"Enter name for Team {i + 1}")
            team_name_input.textChanged.connect(lambda text, idx=i: Custom.update_team_name(team_data, idx, text))
            team_layout.addWidget(team_name_input)

            crest_button = qtw.QPushButton("Select Crest")
            crest_button.clicked.connect(lambda _, idx=i: Custom.select_crest(main_window, idx, team_data))
            team_layout.addWidget(crest_button)

            teams_layout.addLayout(team_layout)

        teams_widget = qtw.QWidget()
        teams_widget.setLayout(teams_layout)

        # Create the team input dialog
        team_dialog = qtw.QDialog(main_window)
        team_dialog.resize(main_window.size())
        team_dialog.setWindowTitle("Enter Team Details")
        team_dialog.setLayout(teams_layout)

        # Add a confirmation button to the team input dialog
        confirm_button = qtw.QPushButton("Add Competition")
        confirm_button.clicked.connect(lambda: Custom.confirm_add_competition(main_window, competition_name, competition_code, competition_crest, team_data, main_layout, team_dialog))
        teams_layout.addWidget(confirm_button)

        team_dialog.exec_()


    @staticmethod
    def select_crest(main_window, team_idx, team_data):
        crest_file, _ = QFileDialog.getOpenFileName(main_window, "Select Team Crest", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")

        if crest_file:
            if len(team_data) <= team_idx:
                team_data.append({'name': '', 'crest': ''})
            team_data[team_idx]['crest'] = crest_file

    @staticmethod
    def update_team_name(team_data, idx, name):
        """
        Update the team name in the team_data list.
        This method is called when the team name input changes.
        """
        if idx >= len(team_data):
            team_data.append({'name': '', 'crest': ''})  
        team_data[idx]['name'] = name

    @staticmethod
    def create_new_fixture():
        CustomQueries.create_new_fixture(Custom.selected_comp_id)

    @staticmethod
    def confirm_add_competition(main_window, competition_name, competition_code, competition_crest, team_data, main_layout, team_dialog):
        if not competition_name or not competition_code or not competition_crest:
            QMessageBox.warning(main_window, "Invalid Input", "Competition name, code, and crest are required.")
            return

        for team in team_data:
            if not team['name'] or not team['crest']:
                QMessageBox.warning(main_window, "Invalid Input", "All teams must have a name and a crest.")
                return

        competition_id = CustomQueries.generate_custom_competition_id()

        competition = {
            'id': competition_id,
            'name': competition_name,
            'code': competition_code,
            'type': 'Custom',
            'emblem': competition_crest
        }

        try:
            Custom.selected_comp_id = competition_id
            CustomQueries.add_to_existing_competitions(competition)

            for team in team_data:
                team_info = {
                    'competition_id': competition_id,
                    'team_name': team['name'],
                    'crest': team['crest']
                }
                CustomQueries.add_team_to_competition(team_info)

            Custom.create_new_fixture()
            QMessageBox.information(main_window, "Success", f"Competition '{competition_name}' with {len(team_data)} teams added successfully!")

            main_window.reload_custom_tab()
            team_dialog.accept()  

        except Exception as e:
            QMessageBox.critical(main_window, "Error", f"Failed to add competition: {str(e)}")


    @staticmethod
    def delete_competition(main_window):
        CustomQueries.delete_competition(Custom.selected_comp_id)
        Custom.selected_comp_id = None
        main_window.reload_custom_tab()
        
    @staticmethod
    def modify_competition(main_window, stacked_layout, main_view_widget):
        modify_layout = qtw.QVBoxLayout()

        add_matches_button = qtw.QPushButton("Add Matches")
        add_matches_button.setStyleSheet("QPushButton { text-align: center; font-size: 14px; padding: 5px 10px; }")
        add_matches_button.clicked.connect(lambda: stacked_layout.setCurrentWidget(main_view_widget))

        modify_layout.addWidget(add_matches_button)

        modify_widget = qtw.QWidget()
        modify_widget.setLayout(modify_layout)

        stacked_layout.addWidget(modify_widget)
        stacked_layout.setCurrentWidget(modify_widget)
        
    @staticmethod
    def create_sub_tab_match(fixtures_layout):
        widget = qtw.QWidget()
        layout = qtw.QVBoxLayout()
    
        matches = CustomQueries.get_fixtures(Custom.selected_comp_id)

        Custom.create_headers(fixtures_layout)

        if matches:
            if isinstance(matches, list): 
                team_rank = 1
                for match in matches:
                    if isinstance(match, dict):
                        Custom.create_custom_match_row(fixtures_layout, match)          
                    else:
                        print(f"Unexpected stat format: {match}")
                        stat_label = qtw.QLabel("Invalid stat format")
                        layout.addWidget(stat_label)
            else:
                print(f"Unexpected stat structure for team stats:")
        else:
            no_match_label = qtw.QLabel("No matches available")
            layout.addWidget(no_match_label)
    
        widget.setLayout(layout)
        return widget

