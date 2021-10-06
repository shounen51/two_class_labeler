import json
import random

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
import numpy as np
from PIL import Image

def load_json(path):
    _dict={}
    try:
        with open(path,encoding="utf-8") as file:
            _dict = json.load(file)
        return True, _dict
    except:
        return False, _dict

def save_json(path, pic_dict):
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(pic_dict, file, indent=4, ensure_ascii=False)
        return True
    except:
        return False

def darw_regions_and_label_list(picPath, _json, frame_label, label_list):
    frame = cv2.imread(picPath)
    frame = frame[...,::-1]
    areas = _json['regions'].keys()
    label_list.clear()
    for i, area in enumerate(areas):
        color = (int(random.random()*205+50), int(random.random()*205+50), int(random.random()*205+50))
        xs = _json['regions'][area]['shape_attributes']['all_points_x']
        ys = _json['regions'][area]['shape_attributes']['all_points_y']
        label = _json['regions'][area]['region_attributes']['label']
        xs = [int(x) for x in xs]
        ys = [int(y) for y in ys]
        img = Image.fromarray(frame)
        frame = np.asarray(img)
        for i in range(1 ,len(xs)):
            cv2.line(frame, (xs[i-1],ys[i-1]), (xs[i],ys[i]), color,2)
        item = QListWidgetItem()
        item.setText(label)
        item.setForeground(QColor(color[0],color[1],color[2]))
        label_list.addItem(item)

    display_video(frame, frame_label)
    return frame

def display_video(frame, label):
    size = (label.width(), label.height())
    width, height = size
    frame = cv2.resize(frame, size, interpolation=cv2.INTER_CUBIC)
    bytesPerComponent = 3
    bytesPerLine = bytesPerComponent * width
    qimg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
    qimg = QPixmap.fromImage(qimg)
    label.setPixmap(qimg)

def display_base64(label, base64):
    ba = QtCore.QByteArray.fromBase64(base64)
    qimg = QImage.fromData(ba, 'PNG')
    qimg = QPixmap.fromImage(qimg)
    label.setPixmap(qimg)

def normalize_points(points, size1, size2=(1920,1080)):
    x_time = size2[0]/size1[0]
    y_time = size2[1]/size1[1]
    new_points = points
    for i ,(x,y) in enumerate(new_points):
        X = int(x*x_time) if int(x*x_time) < size2[0] else size2[0]
        Y = int(y*y_time) if int(y*y_time) < size2[1] else size2[1]
        new_points[i] = (X, Y)
    return new_points
    
# def class_counter(dirpath, pic_dicts):
#     count = {}
#     for cat in _LIST:
#         count[cat] = 0
#     count['unknow'] = 0
#     for pic in pic_dicts.values():
#         for defect in pic['regions'].values():
#             category = defect['region_attributes']['label']
#             try:
#                 count[category] += 1
#             except:
#                 count['unknow'] += 1
#     save_json(os.path.join(dirpath, "category.txt"), count)
