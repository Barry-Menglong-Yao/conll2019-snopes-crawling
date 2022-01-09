"""
A dataset for the coco data which is used by the coco datalaoder
"""
import os
import cv2
import json
import time
import torch
import pickle
import numpy as np
from torchvision.transforms import transforms
from dataloader.transformations import SizeTransformation, PropertyAugmentation, HorizontalFlip
from dataloader.transformations import Rotate, AddWaterMark, Normalize, ToTensor
from torch.utils.data.dataset import Dataset


class CustomDataset(Dataset):
    """The dataset class for custom dataset of interest
    """
    def __init__(self, config:dict, is_train:bool=True):
        """Constructor

        Args:
            config (dict): Configuration parameter Instance
            data_mean (np.ndarray): training data mean
            data_std (np.ndarray): training data std
            is_train (bool, optional): a flag to differentiate between training and validation dataset. Defaults to True.
        """
        self.config = config
        if is_train:
            data_file = "metadata/train_file.txt"
        else:
            data_file = "metadata/val_file.txt"
        with open(data_file, 'r') as f:
            self.image_filenames = [line.strip("\n") for line in f.readlines()]

        if is_train:
            self.transform = transforms.Compose([
                AddWaterMark(),
                SizeTransformation(self.config.parameters),  
                PropertyAugmentation(),
                HorizontalFlip(),
                Rotate(self.config.parameters),
                Normalize(),
                ToTensor()
            ])
        else:
            self.transform = transforms.Compose([
                AddWaterMark(),
                SizeTransformation(self.config.parameters, resize_flag=True),
                Normalize(),
                ToTensor()
            ])
        print("total Images = %d" % len(self.image_filenames))

    def __len__(self) -> int:
        """[summary]
        Returns:
            int: returns the length of the dataset
        """
        return len(self.image_filenames)

    def __getitem__(self, item_index:int) -> torch.Tensor:
        """return a single pre processed image

        Args:
            item_index (int): index of the image to read from the dataset

        Returns:
            torch.Tensor: preprocessed image tensor
        """

        try:
            image = cv2.cvtColor(cv2.imread(self.image_filenames[item_index]), cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(e)
            print("%s image is not readabel" %(self.image_filenames[item_index]))
            raise e


        data = dict()
        data['image'] = image
        data = self.transform(data)

        return data

