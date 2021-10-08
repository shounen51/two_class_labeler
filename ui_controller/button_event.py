import copy
import os

import numpy as np
import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from configs import *
from ui_controller.my_widgets import my_list
from utils.utils import *
from ui.A import A_form
from configs import dataDir, train_data


class btn_events():
    def __init__(self, main_window):
        self.main = main_window
        self.click_point = None
        self.LR = None
        self.focus_list = None
        self.pic_name = "0"
        self.pic_path = ""
        self.last_item = None
        try:
            self.frame = cv2.imread('./src/0.jpg')
        except:
            self.frame = np.zeros((1920,1080,3))

    def ui_ready(self, ui:A_form):
        self.ui = ui

    def list_pics_click(self):
        self.focus_list = self.ui.list_pics
        self.pic_name = self.ui.list_pics.currentItem().text()
        self.pic_path = os.path.join(dataDir, self.pic_name)
        self.frame = cv2.imread(self.pic_path)
        display_video(self.frame[:,:,::-1], self.ui.lab_pic)

    def list_label_click(self, list_widget:my_list):
        self.focus_list = list_widget
        self.LR = None
        self.pic_name = self.focus_list.currentItem().text()
        if self.focus_list == self.ui.list_L:
            self.pic_path = os.path.join("./train_data/L/", self.pic_name)
        else:
            self.pic_path = os.path.join("./train_data/R/", self.pic_name)
        self.frame = cv2.imread(self.pic_path)
        display_video(self.frame[:,:,::-1], self.ui.lab_pic)

    def btn_del_click(self):
        if self.focus_list == self.ui.list_pics or self.focus_list == None:
            return
        self._del_pic()
        print(self.ui.list_pics.currentRow())
        if self.focus_list.currentRow() >= 0 and self.focus_list.currentRow() != self.focus_list.count():
            self.list_label_click(self.focus_list)

    def list_row_changed(self, list_widget:my_list):
        if self.last_item != None:
            self.last_item.setBackground(QColor("#424242"))
        if list_widget.currentRow() >= 0:
            self.last_item = list_widget.currentItem()
            self.last_item.setBackground(QColor("#ff2020"))
        else:
            self.last_item == None

    def label_press(self, point, LR):
        if self.focus_list == self.ui.list_pics:
            self.LR = LR
            self.click_point = point

    def label_move(self, point):
        if self.LR == None or not self.ui.cb_box.isChecked():
            return
        point = self._limit_point(point)
        color = (0,0,255) if self.LR == "L" else (0,255,0)
        drew = copy.copy(self.frame)
        p1 = [self.click_point[0], self.click_point[1]]
        p2 = [point[0], point[1]]
        ori_h, ori_w, _ = self.frame.shape
        p1, p2 = normalize_points([p1, p2], (self.ui.lab_pic.width(), self.ui.lab_pic.height()), (ori_w, ori_h))
        cv2.rectangle(drew, p1, p2, color, 3)
        display_video(drew[:,:,::-1], self.ui.lab_pic) 

    def label_release(self, point):
        if self.LR == None:
            return
        if self.ui.cb_box.isChecked():
            patch = self._box_patch(point)
        else:
            patch = self.frame
        dir = os.path.join(train_data, self.LR)
        path = os.path.join(dir, self.pic_name)
        cv2.imwrite(path, patch)
        list_widget = self.ui.list_L if self.LR == 'L' else self.ui.list_R
        list_widget.addItem(self.pic_name)
        self.LR = None

        if self.ui.list_pics.currentRow()+1 != self.ui.list_pics.count():
            self.ui.list_pics.setCurrentRow(self.ui.list_pics.currentRow()+1)
            self.list_pics_click()

    def _box_patch(self, point):
        point = self._limit_point(point)
        if point[0] == self.click_point[0] or point[1] == self.click_point[1]:
            display_video(self.frame[:,:,::-1], self.ui.lab_pic) 
            return
        p1 = [min(self.click_point[0], point[0]), min(self.click_point[1], point[1])]
        p2 = [max(self.click_point[0], point[0]), max(self.click_point[1], point[1])]
        ori_h, ori_w, _ = self.frame.shape
        p1, p2 = normalize_points([p1, p2], (self.ui.lab_pic.width(), self.ui.lab_pic.height()), (ori_w, ori_h))
        patch = self.frame[p1[1]:p2[1],p1[0]:p2[0],:]
        return patch

    def _del_pic(self):
        try:
            os.remove(self.pic_path)
            self.focus_list.takeItem(self.focus_list.currentRow())
        except:
            return

    def _limit_point(self, point):
        temp = []
        for p in point:
            if p > 0:
                temp.append(p)
            else:
                temp.append(0)
        return temp