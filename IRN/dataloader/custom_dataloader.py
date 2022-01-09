import time
import torch
import numpy as np
from typing import List, Dict
from torch.utils.data.dataloader import DataLoader
from dataset.custom_dataset import CustomDataset


class CustomDataLoader(DataLoader):
    def __init__(self, config:dict, nproc:int=1):
        """Constructor 

        Args:
            config (dict): Configuration parameter Instance
            nproc (int, optional): [description]. Defaults to 1.
        """
        train_dataset = CustomDataset(config, is_train=True)
        val_dataset = CustomDataset(config, is_train=False)
        batch_size = config.parameters['batch_size']
        self.train_dataloader = DataLoader(train_dataset,  batch_size=batch_size, shuffle=False, 
                                            num_workers=nproc, pin_memory=False)
        self.val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, 
                                        num_workers=nproc, pin_memory=False)

    def get_loader(self) -> List[DataLoader]:
        """A method to access the dataloaders

        Returns:
            List[DataLoader]: training and validation dataloader
        """
        return [self.train_dataloader, self.val_loader]

