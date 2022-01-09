import cv2
import time
import torch
import torchvision
import numpy as np
from typing import List
from threading import Thread
import torch.nn.functional as F


class Visualization:
    def __init__(self, writer, config):
        self.config = config
        self.writer = writer
        self.count = config.parameters['viz_image_count']
        self.image_size = self.config.parameters['image_size']

    def plot(self, images, prediction, targets, step):
        image_grid = torchvision.utils.make_grid(images[0:4], padding=5)
        pred_grid = torchvision.utils.make_grid(prediction[0:4], padding=5)
        gt_grid = torchvision.utils.make_grid(targets[0:4], padding=5)

        self.writer.add_image("Images", image_grid, global_step=step)
        self.writer.add_image("Reconstructed Images", pred_grid, global_step=step)
        self.writer.add_image("Ground Truth Images", gt_grid, global_step=step)