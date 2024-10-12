import sys
import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
import PyQt5.QtCore as qtc
from UILoader import UILoader  
#import API_Call

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("IFootball")
        self.setGeometry(400, 100, 500, 800)
        self.setLayout(qtw.QVBoxLayout())

        self.stack = qtw.QStackedWidget(self)

        # Add the different pages (tabs)
        self.stack.addWidget(UILoader.create_home_tab())
        self.stack.addWidget(UILoader.create_match_tab(self))
        self.stack.addWidget(UILoader.create_favorite_tab(self))
        self.stack.addWidget(UILoader.create_stats_tab(self))

        self.layout().addWidget(self.stack)

        # Create bottom tab buttons
        self.tab_bar_layout = qtw.QHBoxLayout()
        self.home_button = UILoader.create_bottom_tab(self, "Home", "Images/home_uc.png", "Images/home_c.png")
        self.match_button = UILoader.create_bottom_tab(self, "Match", "Images/whistle_uc.png", "Images/whistle_c.png")
        self.favorite_button = UILoader.create_bottom_tab(self, "Favorite", "Images/abc.png", "Images/bcd.png")
        self.stats_button = UILoader.create_bottom_tab(self, "Stats", "Images/stats_uc.png", "Images/stats_c.png")

        # Add buttons to the tab bar layout
        self.tab_bar_layout.addWidget(self.home_button)
        self.tab_bar_layout.addWidget(self.match_button)
        self.tab_bar_layout.addWidget(self.favorite_button)
        self.tab_bar_layout.addWidget(self.stats_button)

        # Add bottom tab bar layout to main layout
        self.layout().addLayout(self.tab_bar_layout)

        # Initial selection (set the home button as active initially)
        self.update_active_tab(self.home_button, 0)

        self.show()

    # Switch between tabs and update the active tab
    def switch_tab(self, selected_button):
        if selected_button == self.home_button:
            self.update_active_tab(self.home_button, 0)
        elif selected_button == self.match_button:
            self.update_active_tab(self.match_button, 1)
        elif selected_button == self.favorite_button:
            self.update_active_tab(self.favorite_button, 2)
        elif selected_button == self.stats_button:
            self.update_active_tab(self.stats_button, 3)

    # Update the appearance of the active tab
    def update_active_tab(self, active_button, index):
        self.reset_button(self.home_button)
        self.reset_button(self.match_button)
        self.reset_button(self.favorite_button)
        self.reset_button(self.stats_button)

        active_button.setIcon(qtg.QIcon(active_button.icon_path_selected))
        active_button.setStyleSheet("QPushButton { text-align: center; color: black; font-weight: bold; }")
        self.stack.setCurrentIndex(index)

    # Reset a button to its default state
    def reset_button(self, button):
        button.setIcon(qtg.QIcon(button.icon_path_default))
        button.setStyleSheet("QPushButton { text-align: center; color: grey; }")

# Run the application
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
