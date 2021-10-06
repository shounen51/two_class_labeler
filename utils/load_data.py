import os

from configs import dataDir, train_data

class data_loader():
    def __init__(self, rootDir):
        self.rootDir = rootDir
        self.pic_list = []
        os.makedirs(dataDir, exist_ok=True)
        os.makedirs(os.path.join(train_data, 'L'), exist_ok=True)
        os.makedirs(os.path.join(train_data, 'R'), exist_ok=True)
        self._load_json()

    def _load_json(self):
        for _file in os.listdir(self.rootDir):
            pic = os.path.join(self.rootDir,_file)
            if pic.endswith('.png') or pic.endswith('.jpg'):
                self.pic_list.append(_file)

    def get_pics_num(self):
        return len(self.pic_list)

    def get_pics(self):
        return self.pic_list
