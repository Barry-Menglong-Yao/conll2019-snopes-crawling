import torch
import math
import torch.nn as nn
from typing import List
from torch.nn import BatchNorm2d
from network.layers.encoder_block import EncoderBlock

class Encoder(nn.Module):
    def __init__(self):
        """Constructor

        Args:
            nc (int, optional): number of classes. Defaults to 90.
            n_anchors (int, optional): number of anchors. Defaults to 3.
        """
        super(Encoder, self).__init__()
        self.conv1 = EncoderBlock(3, 64, 7, 2)
        self.conv2 = EncoderBlock(64, 128, 3, 2)
        self.conv3 = EncoderBlock(128, 256, 3, 2)
        self.conv4 = EncoderBlock(256, 512, 3, 2)
        self.conv5 = EncoderBlock(512, 512, 3, 2)

    def forward(self, x:torch.Tensor) -> List[torch.Tensor]:
        """Forward pass of the network module

        Args:
            x (torch.Tensor): Input Tensor

        Returns:
            torch.Tensor: Output Tensor
        """
        c1 = self.conv1(x)
        c2 = self.conv2(c1)
        c3 = self.conv3(c2)
        c4 = self.conv4(c3)
        c5 = self.conv5(c4)

        return c3, c4, c5