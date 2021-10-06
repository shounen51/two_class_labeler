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

def add_in_data(data_json, _data):
    with open(data_json, "w") as _j:
        _str = json.dumps(_data, ensure_ascii=False)
        _j.write(_str)

def label2int(label, _LIST):
    if label in _LIST:
        return _LIST.index(label)
    else:
        return -1


class make_json(QThread):
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
        self.main.set_button_red("Detectron")
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

                            _dict = {}
                            picPath = os.path.join(_dir,pic)
                            frame = cv2.imread(picPath)
                            _dict['width'] = frame.shape[1]
                            _dict['height'] = frame.shape[0]
                            _dict["file_name"] = pic
                            _dict["id"] = pic
                            areas = _json[pic]['regions'].keys()
                            _json[pic]["filename"]  = os.path.join("data/detectron2/all/", _json[pic]["filename"])
                            objs = []
                            for i, area in enumerate(areas):
                                obj = {}
                                color = (int(random.random()*205+50), int(random.random()*205+50), int(random.random()*205+50))
                                xs = _json[pic]['regions'][area]['shape_attributes']['all_points_x']
                                ys = _json[pic]['regions'][area]['shape_attributes']['all_points_y']
                                label = _json[pic]['regions'][area]['region_attributes']['label']
                                xs = [int(x) for x in xs]
                                ys = [int(y) for y in ys]
                                bbox = [min(xs), min(ys), max(xs), max(ys)]
                                obj["bbox"] = bbox
                                segmentation = []
                                for i, x in enumerate(xs):
                                    segmentation.append(x)
                                    segmentation.append(ys[i])
                                obj["segmentation"] = [segmentation]
                                obj['bbox_mode'] = 0
                                obj["category_id"] = label2int(label, _LIST)
                                number_dict[label] += 1
                                img = Image.fromarray(frame)
                                draw = ImageDraw.Draw(img)
                                fontStyle = ImageFont.truetype("font/simsun.ttc", 24, encoding="utf-8")
                                draw.text((10, 10+i*30), label, color, font=fontStyle)
                                frame = np.asarray(img)
                                for i in range(1 ,len(xs)):
                                    cv2.line(frame, (xs[i-1],ys[i-1]), (xs[i],ys[i]), color,2)
                                objs.append(obj)
                            _dict["annotations"] = objs
                            shutil.copyfile(picPath, _json[pic]["filename"])
                            _set.append(_dict)
        add_in_data("./data/detectron2" + "/train.json", train_list)
        add_in_data("./data/detectron2" + "/test.json", test_list)
        print("pics count: " ,str(count))
        for key in number_dict:
            print(key + ":" + str(number_dict[key]))
        self.main.set_button_back("Detectron")
        print("\ndetectron2 OK")


