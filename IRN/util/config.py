import yaml
import numpy as np
import matplotlib
import matplotlib.cm


class Config:
    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.parameters = {}
        self.class_to_labels = {}
        self.labels_to_class = {}
        self.cmap = matplotlib.cm.get_cmap('jet')
        self.class_colors = {}
        self.text_colors = {}

    def load_config(self):
        self.parameters = self.read_yaml(self.config_dir+"/parameters.yaml")
        
    @staticmethod
    def read_yaml(filename):
        with open(filename, "r") as file:
            return yaml.load(file, yaml.FullLoader)

    def map_class_labels_coco(self):
        with open(self.config_dir+"/coco.names.txt",  "r") as f:
            classes = [cls.strip() for cls in f.readlines()]

        # create a mapping of the class
        for i, c in enumerate(classes):
            self.labels_to_class[i] = c
            self.class_to_labels[c] = i
            self.class_colors[i] = np.uint8(255*np.array(self.cmap(((i+1)*10)%255)))
            self.text_colors[i] = 255 - self.class_colors[i]

    def map_class_labels_pascal(self):
        classes = ['person', 'bird', 'cat', 'cow', 'dog', 'horse', 'sheep', 'aeroplane', 'bicycle', 'boat', 'bus',
                   'car', 'motorbike', 'train', 'bottle', 'chair', 'diningtable', 'pottedplant', 'sofa', 'tvmonitor']

        # create a mapping of the class
        for i, c in enumerate(classes):
            self.labels_to_class[i] = c
            self.class_to_labels[c] = i
            self.class_colors[i] = np.uint8(255*np.array(self.cmap(((i+1)*10)%255)))
            self.text_colors[i] = 255 - self.class_colors[i]

