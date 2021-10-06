# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Joseph\git\Taipei_MOT_UI\test\A.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from ui.color import *
from ui_controller.my_widgets import *

from utils.utils import display_base64
from src.main_jpg import main_jpg

class A_form(QtWidgets.QWidget):
    def __init__(self, Form, main, event):
        QtWidgets.QWidget.__init__(self)
        # Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setObjectName("Form")
        Form.resize(1460, 920)
        Form.setMinimumSize(QtCore.QSize(1920, 1080))
        Form.setMaximumSize(QtCore.QSize(1920, 1080))
        Form.setAutoFillBackground(True)
        Form.setPalette(back_plt)

        font = QtGui.QFont()
        font.setFamily("微軟正黑體")
        font.setPointSize(20)

        self.lab_title = my_label(Form)
        self.lab_title.setFont(font)
        self.lab_title.setGeometry(QtCore.QRect(270, 10, 1391, 91))
        self.lab_title.setObjectName("label")
        self.lab_title.setAlignment(QtCore.Qt.AlignCenter)
        self.list_pics = my_list(Form)
        self.list_pics.setFont(font)
        self.list_pics.setGeometry(QtCore.QRect(10, 110, 251, 841))
        self.list_pics.setObjectName("listWidget")
        self.list_pics.setSortingEnabled(True)
        self.lab_pic = clickable_label(Form, event)
        self.lab_pic.setGeometry(QtCore.QRect(270, 110, 1371, 771))
        self.lab_pic.setObjectName("label_2")
        display_base64(self.lab_pic, main_jpg)
        # self.lab_pic.setStyleSheet("background-image: url(./src/0.jpg);")
        self.list_L = my_list(Form)
        self.list_L.setGeometry(QtCore.QRect(1660, 110, 251, 420))
        self.list_L.setObjectName("listWidget")
        self.list_L.setFont(font)
        self.list_R = my_list(Form)
        self.list_R.setFont(font)
        self.list_R.setGeometry(QtCore.QRect(1660, 540, 251, 420))
        self.list_R.setObjectName("listWidget")
        self.btn_del = my_btn(Form)
        self.btn_del.setFont(font)
        self.btn_del.setGeometry(QtCore.QRect(1660, 980, 251, 61))
        self.btn_del.setObjectName("pushButton_2")


        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.event_connect(event)

    def event_connect(self, event):
        self.list_pics.itemClicked.connect(event.list_pics_click)
        self.list_L.itemClicked.connect(lambda:event.list_label_click(self.list_L))
        self.list_R.itemClicked.connect(lambda:event.list_label_click(self.list_R))
        self.list_pics.currentRowChanged.connect(lambda:event.list_row_changed(self.list_pics))
        self.list_L.currentRowChanged.connect(lambda:event.list_row_changed(self.list_L))
        self.list_R.currentRowChanged.connect(lambda:event.list_row_changed(self.list_R))
        self.btn_del.clicked.connect(event.btn_del_click)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Hand in pocket 標註工具"))
        self.btn_del.setText(_translate("Form", "刪除標註"))


