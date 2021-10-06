import json
import numpy as np
import os
import shutil
import random
import cv2
from PIL import Image, ImageDraw, ImageFont
from configs import _LIST
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from configs import train_set

def load_json(path):
    _dict={}
    with open(path,encoding="utf-8") as file:
        _dict = json.load(file)
    return _dict

def make_pic_txt(pic_name, obj_list):
    with open(pic_name, "w") as txt:
        _str = ""
        for obj in obj_list:
            _str += " ".join([str(cxy) for cxy in obj]) + "\n"
        txt.write(_str)

def make_trainval_txt(path, tv_list):
    with open(path, "w") as txt:
        _str = "\n".join(tv_list)
        txt.write(_str)

def label2int(label, _LIST):
    if label in _LIST:
        return _LIST.index(label)
    else:
        return -1

class make_txt(QThread):
    def __init__(self, main, parent=None):
        super().__init__(parent)
        self.rootDir = ""
        self.main = main
        self.train_set = train_set
        self.pics_name = []

    def setting(self, rootDir, train):
        self.rootDir = rootDir
        self.train_set = train

    def run(self):
        rootDir = self.rootDir
        self.main.set_button_red("Yolo")
        number_dict = {}
        for key in _LIST:
            number_dict[key] = 0
        train_list = []
        test_list = []
        nAll = 0
        nTrain = 0
        nTset = 0
        count = 0
        rootDir.replace('\\','\\\\')
        for _file in os.listdir(rootDir):
            _dir = os.path.join(rootDir,_file)
            if os.path.isdir(_dir):
                for path in os.listdir(_dir):
                    if path.split('.')[-1]=='json':
                        jsonPath = os.path.join(_dir,path)
                        _json = load_json(jsonPath)
                        keys=_json.keys()
                        nAll = len(keys)
                        count += nAll
                        nTrain = nAll*self.train_set
                        nTset = nAll-nTrain

                        for pic in keys:
                            _rand = random.randint(1, nTrain+nTset)
                            if _rand > nTrain:
                                nTset-=1
                                _set = test_list
                            else:
                                nTrain-=1
                                _set = train_list
                            if pic in self.pics_name:
                                continue
                            else:
                                self.pics_name.append(pic)
                            picPath = os.path.join(_dir,pic)
                            frame = cv2.imread(picPath)
                            width = frame.shape[1]
                            height = frame.shape[0]
                            areas = _json[pic]['regions'].keys()
                            pic_path = os.path.join("data/yolov4/images/", _json[pic]["filename"])
                            txt_path = os.path.join("data/yolov4/images/", _json[pic]["filename"].replace(".jpg",".txt"))
                            objs = []
                            for i, area in enumerate(areas):
                                obj = []
                                color = (int(random.random()*205+50), int(random.random()*205+50), int(random.random()*205+50))
                                xs = _json[pic]['regions'][area]['shape_attributes']['all_points_x']
                                ys = _json[pic]['regions'][area]['shape_attributes']['all_points_y']
                                label = _json[pic]['regions'][area]['region_attributes']['label']
                                xs = [int(x) for x in xs]
                                ys = [int(y) for y in ys]
                                xyxy_ori = [min(xs), min(ys), max(xs), max(ys)]
                                xywh = [
                                    round(((xyxy_ori[0]+xyxy_ori[2])/2)/width, 6),
                                    round(((xyxy_ori[1]+xyxy_ori[3])/2)/height, 6),
                                    round((xyxy_ori[2]-xyxy_ori[0])/width,6),
                                    round((xyxy_ori[3]-xyxy_ori[1])/height,6)
                                ]
                                cat = label2int(label, _LIST)
                                number_dict[label] += 1
                                obj.append(cat)
                                obj += xywh
                                objs.append(obj)
                            shutil.copyfile(picPath, pic_path)
                            make_pic_txt(txt_path, objs)
                            _set.append(pic_path)
        make_trainval_txt("data/yolov4" + "/train.txt", train_list)
        make_trainval_txt("data/yolov4" + "/test.txt", test_list)
        print("pics count: " ,str(count))
        for key in number_dict:
            print(key + ":" + str(number_dict[key]))
        self.main.set_button_back("Yolo")
        print("\nyolov4 OK")


