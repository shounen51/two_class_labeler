import os

from configs import dataDir, train_data

class data_loader():
    def __init__(self, rootDir):
        self.rootDir = rootDir
        self.L_dir = os.path.join(train_data, 'L')
        self.R_dir = os.path.join(train_data, 'R')
        self.pic_list = []
        self.L_list = []
        self.R_list = []
        os.makedirs(dataDir, exist_ok=True)
        os.makedirs(self.L_dir, exist_ok=True)
        os.makedirs(self.R_dir, exist_ok=True)
        self._load_json()
        self._load_label()        
        self.gray_pic = [p for p in (self.L_list + self.R_list) if p in self.pic_list]

    def _load_json(self):
        for _file in os.listdir(self.rootDir):
            pic = os.path.join(self.rootDir,_file)
            if pic.endswith('.png') or pic.endswith('.jpg'):
                self.pic_list.append(_file)

    def _load_label(self):
        for _file in os.listdir(self.L_dir):
            pic = os.path.join(self.L_dir,_file)
            if pic.endswith('.png') or pic.endswith('.jpg'):
                self.L_list.append(_file)
        for _file in os.listdir(self.R_dir):
            pic = os.path.join(self.R_dir,_file)
            if pic.endswith('.png') or pic.endswith('.jpg'):
                self.R_list.append(_file)

    def get_pics_num(self):
        return len(self.pic_list)

    def get_pics(self):
        return self.pic_list
