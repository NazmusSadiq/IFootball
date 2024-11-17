import sys
import json
import os
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from UILoader import UILoader 
from Queries import Queries
import API_Call
import Scraper
from Matches import Matches

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IFootball")
        self.setGeometry(400, 100, 600, 900)
        self.setLayout(qtw.QVBoxLayout())

        self.stack = qtw.QStackedWidget(self)

        # Create tabs once and store them in variables
        self.home_tab = UILoader.create_home_tab()
        self.match_tab = UILoader.create_match_tab(self)
        self.favorite_tab = UILoader.create_favorite_tab(self)
        self.stats_tab = UILoader.create_stats_tab(self)

        # Add these widgets to the stack
        self.stack.addWidget(self.home_tab)
        self.stack.addWidget(self.match_tab)
        self.stack.addWidget(self.favorite_tab)
        self.stack.addWidget(self.stats_tab)

        self.layout().addWidget(self.stack)

        self.tab_bar_layout = qtw.QHBoxLayout()
        self.home_button = UILoader.create_bottom_tab(self, "Home", "Images/home_uc.png", "Images/home_c.png")
        self.match_button = UILoader.create_bottom_tab(self, "Match", "Images/whistle_uc.png", "Images/whistle_c.png")
        fav_id = Queries.fav_team_id
        crest_pixmap = Matches.get_team_crest(fav_id, 1)
        self.favorite_button = UILoader.create_bottom_tab(self, "Favorite", crest_pixmap, crest_pixmap)
        self.stats_button = UILoader.create_bottom_tab(self, "Stats", "Images/stats_uc.png", "Images/stats_c.png")

        self.tab_bar_layout.addWidget(self.home_button)
        self.tab_bar_layout.addWidget(self.match_button)
        self.tab_bar_layout.addWidget(self.favorite_button)
        self.tab_bar_layout.addWidget(self.stats_button)

        self.layout().addLayout(self.tab_bar_layout)

        self.update_active_tab(self.home_button, 0)

        self.show()

    def switch_tab(self, selected_button):
        if selected_button == self.home_button:
            self.update_active_tab(self.home_button, 0)
        elif selected_button == self.match_button:
            self.update_active_tab(self.match_button, 1)
        elif selected_button == self.favorite_button:
            self.update_active_tab(self.favorite_button, 2)
        elif selected_button == self.stats_button:
            self.update_active_tab(self.stats_button, 3)

    def update_active_tab(self, active_button, index):
        self.reset_button(self.home_button)
        self.reset_button(self.match_button)
        self.reset_button(self.favorite_button)
        self.reset_button(self.stats_button)
        active_button.setIcon(qtg.QIcon(active_button.icon_path_selected))
        active_button.setStyleSheet("QPushButton { text-align: center; color: black; font-weight: bold; }")
        self.stack.setCurrentIndex(index)
        fav_id = Queries.fav_team_id
        crest_pixmap = Matches.get_team_crest(fav_id, 1)
        self.favorite_button.setIcon(qtg.QIcon(crest_pixmap))

    def reset_button(self, button):
        button.setIcon(qtg.QIcon(button.icon_path_default))
        button.setStyleSheet("QPushButton { text-align: center; color: grey; }")

    def reload_everything(self):
        for i in reversed (range(self.stack.count())):
            widget = self.stack.widget(i)
            if widget:
                self.stack.removeWidget(widget)
                widget.deleteLater() 

        self.home_tab = UILoader.create_home_tab()
        self.match_tab = UILoader.create_match_tab(self)
        self.favorite_tab = UILoader.create_favorite_tab(self)
        self.stats_tab = UILoader.create_stats_tab(self)

        self.stack.addWidget(self.home_tab)
        self.stack.addWidget(self.match_tab)
        self.stack.addWidget(self.favorite_tab)
        self.stack.addWidget(self.stats_tab)
        self.update_active_tab(self.favorite_button, 2)

        self.stack.setCurrentWidget(self.favorite_tab)  

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
