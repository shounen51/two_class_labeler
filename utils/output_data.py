import json
import numpy as np
import os
import shutil
import random
import cv2
from PIL import Image, ImageDraw, ImageFont
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

def add_in_data(data_json, _data):
    with open(data_json, "w") as _j:
        _str = json.dumps(_data, ensure_ascii=False)
        _j.write(_str)

def label2int_switch(label):
    return label_map[label]


class make_json(QThread):
    def __init__(self, main, _list,parent=None):
        super().__init__(parent)
        self.rootDir = ""
        self.main = main
        self.train_set = train_set
        self.all_labels = {}
        self.train_list = []
        self.test_list = []
        self.other_option = False
        self._LIST = _list
        

    def setting(self, rootDir, train, other_option):
        self.other_option = other_option
        self.rootDir = rootDir
        self.train_set = train

    
    def _label2int(self, label):
        if label in self._LIST:
            return self._LIST.index(label)
        else:
            print('有例外label')
            return -1

    def _collect_label(self):
        shutil.rmtree('train_data/yolov5_data/images/')
        shutil.rmtree('train_data/yolov5_data/labels/')
        os.mkdir('train_data/yolov5_data/images/')
        os.mkdir('train_data/yolov5_data/labels/')
        os.mkdir('train_data/yolov5_data/images/train/')
        os.mkdir('train_data/yolov5_data/images/val/')
        os.mkdir('train_data/yolov5_data/labels/train/')
        os.mkdir('train_data/yolov5_data/labels/val/')
        if not os.path.isdir('train_data/yolov4/images/'):
            os.mkdir('train_data/yolov4/images/')
        if not os.path.isdir('train_data/detectron2/all/'):
            os.mkdir('train_data/detectron2/all/')
        rootDir = self.rootDir
        rootDir.replace('\\','\\\\')
        for _file in os.listdir(rootDir):
            _dir = os.path.join(rootDir,_file)
            if os.path.isdir(_dir):
                for path in os.listdir(_dir):
                    if path.split('.')[-1]=='json' or path.split('.')[-1]=='txt':
                        jsonPath = os.path.join(_dir,path)
                        _json = load_json(jsonPath)
                        keys = _json.keys()
                        for pic in keys:
                            self.all_labels[pic] = _json[pic]
                            picPath = os.path.join(_dir,pic)
                            shutil.copyfile(picPath, os.path.join("train_data/yolov4/images/", _json[pic]["filename"]))
                            shutil.copyfile(picPath, os.path.join("train_data/detectron2/all/", _json[pic]["filename"]))
        keys = self.all_labels.keys()
        nAll = len(keys)
        nTrain = nAll*self.train_set
        nTset = nAll-nTrain
        for pic in keys:
            _rand = random.randint(1, nTrain+nTset)
            if _rand > nTrain:
                nTset-=1
                self.test_list.append(pic)
            else:
                nTrain-=1
                self.train_list.append(pic)


    def _darknet_data(self):
        rootDir = self.rootDir
        rootDir.replace('\\','\\\\')
        number_dict = {}
        for key in self._LIST:
            number_dict[key] = 0
        train_list = [os.path.join('train_data/yolov4/images/' + pic) for pic in self.train_list]
        test_list = [os.path.join('train_data/yolov4/images/' + pic) for pic in self.test_list]
        keys = self.all_labels.keys()
        for pic in keys:
            picPath = os.path.join('train_data/yolov4/images/', pic)
            frame = cv2.imread(picPath)
            width = frame.shape[1]
            height = frame.shape[0]
            areas = self.all_labels[pic]['regions'].keys()
            pic_path = os.path.join("train_data/yolov4/images/", self.all_labels[pic]["filename"])
            txt_path = os.path.join("train_data/yolov4/images/", self.all_labels[pic]["filename"].replace(self.all_labels[pic]["filename"].split('.')[-1], "txt"))
            objs = []
            for i, area in enumerate(areas):
                obj = []
                color = (int(random.random()*205+50), int(random.random()*205+50), int(random.random()*205+50))
                xs = self.all_labels[pic]['regions'][area]['shape_attributes']['all_points_x']
                ys = self.all_labels[pic]['regions'][area]['shape_attributes']['all_points_y']
                label = self.all_labels[pic]['regions'][area]['region_attributes']['label']
                xs = [int(x) for x in xs]
                ys = [int(y) for y in ys]
                xyxy_ori = [max(0,min(xs)), max(0,min(ys)), min(width,max(xs)), min(height,max(ys))]
                xywh = [
                    round(((xyxy_ori[0]+xyxy_ori[2])/2)/width, 6),
                    round(((xyxy_ori[1]+xyxy_ori[3])/2)/height, 6),
                    round((xyxy_ori[2]-xyxy_ori[0])/width,6),
                    round((xyxy_ori[3]-xyxy_ori[1])/height,6)
                ]
                cat = self._label2int(label)
                if cat < 0 or cat > 8:
                    print(pic)
                number_dict[label] += 1
                obj.append(cat)
                obj += xywh
                objs.append(obj)
            make_pic_txt(txt_path, objs)
            """yolov5"""
            if pic in self.train_list:
                shutil.copyfile(picPath, os.path.join("train_data/yolov5_data/images/train", pic))
                make_pic_txt(os.path.join("train_data/yolov5_data/labels/train", pic.replace(pic.split('.')[-1], "txt")), objs)
            else:
                shutil.copyfile(picPath, os.path.join("train_data/yolov5_data/images/val", pic))
                make_pic_txt(os.path.join("train_data/yolov5_data/labels/val", pic.replace(pic.split('.')[-1], "txt")), objs)


        make_trainval_txt("train_data/yolov4" + "/train.txt", train_list)
        make_trainval_txt("train_data/yolov4" + "/test.txt", test_list)
        for key in number_dict:
            print(key + ":" + str(number_dict[key]))
        print("yolov4 OK")

    def _detectron_data(self):
        keys = self.all_labels.keys()
        train_list = []
        test_list = []
        number_dict = {}
        for key in self._LIST:
            number_dict[key] = 0
        for pic in keys:
            if pic in self.test_list:
                _set = test_list
            else:
                _set = train_list

            _dict = {}
            picPath = os.path.join('train_data/detectron2/all/', pic)
            frame = cv2.imread(picPath)
            _dict['width'] = frame.shape[1]
            _dict['height'] = frame.shape[0]
            _dict["file_name"] = pic
            _dict["id"] = pic
            areas = self.all_labels[pic]['regions'].keys()
            objs = []
            for i, area in enumerate(areas):
                obj = {}
                color = (int(random.random()*205+50), int(random.random()*205+50), int(random.random()*205+50))
                xs = self.all_labels[pic]['regions'][area]['shape_attributes']['all_points_x']
                ys = self.all_labels[pic]['regions'][area]['shape_attributes']['all_points_y']
                label = self.all_labels[pic]['regions'][area]['region_attributes']['label']
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
                l = self._label2int(label)
                if self.other_option:
                    l = label2int_switch(l)
                    if l < 0:
                        continue
                obj["category_id"] = l
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
            _set.append(_dict)
        add_in_data("./train_data/detectron2" + "/train.json", train_list)
        add_in_data("./train_data/detectron2" + "/test.json", test_list)
        for key in number_dict:
            print(key + ":" + str(number_dict[key]))
        print("detectron2 OK")

    def run(self):
        self.main.set_button_red()
        self._collect_label()
        self._detectron_data()
        self._darknet_data()
        self.main.set_button_back()

