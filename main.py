'''
⠄⠄⠈⣿⠄⠄⠄⢙⢞⢿⣿⢹⢿⣦⢏⣱⢿⠘⣿⣝⠹⢿⣿⡽⣿⣿⣏⣆⢿⣿⡞⠁
⠄⠄⠄⢻⡀⠄⠄⠈⣾⡸⡏⢸⡾⣴⣿⣿⣶⣼⣎⢵⢀⡛⣿⣷⡙⡻⢻⡴⠨⠨⠖⠃
⠄⠄⠄⠈⣧⢀⡴⠊⢹⠁⡇⠈⢣⣿⣿⣿⣿⣦⣿⣷⣜⡳⣝⢧⢃⢣⣼⢁⠘⠆⠄⠄
⠄⠄⠄⠄⢹⡇⠄⣠⠔⠚⣅⠄⢰⣶⣦⣭⣿⣿⣿⡿⠟⠿⣷⡧⠄⣘⣟⣸⠄⠄⠄⠄
⠄⠄⠄⠄⠄⢷⠎⠄⠄⠄⣼⣦⠻⣿⣿⡟⠛⠻⢿⣿⣿⣿⡾⢱⣿⡏⠸⡏⠄⠄⠄⠄
⠄⠄⠄⠄⠄⠸⡄⠄⡄⠄⣿⢧⢗⠌⠻⣇⠿⠿⣸⣿⣿⡟⡐⣿⠟⢰⣇⠇⠄⠄⠄⠄
⠄⠄⠄⠄⠄⣠⡆⠄⠃⢠⠏⣤⢀⢢⡰⣭⣛⡉⠩⠭⡅⣾⢳⡴⡀⢸⣿⡆⠄⠄⠄⠄
⠄⠄⠄⢀⣶⡟⣽⠼⢀⡕⢀⠘⠸⢮⡳⡻⡍⡷⡆⠤⠤⠭⢸⢳⣷⢸⡟⣷⠄⠄⠄⠄
'''

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui.A import A_form
from ui_controller.button_event import btn_events
from utils.load_data import data_loader
from configs import dataDir

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.data_dict = data_loader(dataDir)
        self.event = btn_events(self)
        self.ui = A_form(self, self, self.event)
        self.event.ui_ready(self.ui)
        self.ui.list_pics.addItems(self.data_dict.get_pics())
        self.ui.list_L.addItems(self.data_dict.L_list)
        self.ui.list_R.addItems(self.data_dict.R_list)
        self.ui.lab_title.setText("pics:" + str(self.data_dict.get_pics_num()))
        for p in self.data_dict.gray_pic:
            items = self.ui.list_pics.findItems(p,Qt.MatchFlag.MatchExactly)
            for item in items:
                item.setBackground(QColor("#424242"))
        if self.ui.list_pics.count() > 0:
            self.ui.list_pics.setCurrentRow(0)
            self.event.list_pics_click()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())